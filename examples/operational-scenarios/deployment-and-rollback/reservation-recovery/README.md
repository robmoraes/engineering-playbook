# Measure recovery after a booking deployment fails

The API is running and its readiness check can read PostgreSQL, but customers
cannot create reservations. In this disposable deployment, the candidate
image stays the same while a database access configuration changes. Restore
the specific permission that failed and verify the result through the HTTP
route a customer uses.

## Build, test and deploy

The [CI workflow](../../../../.github/workflows/reservation-recovery.yml)
builds the [reservation service](../../../reference-implementations/small-production-service/reservations/README.md)
once from a recorded Git revision. It runs the API/worker contention test
against that image, then starts the recovery drill in a separate Compose
project with its own database volume. The API and worker container image
IDs must match the tested image ID. A tag alone would also identify another
build if someone moved the tag.

The workflow runs on pull requests that affect the service or the executable
drill. To repeat it on the default branch, select the reservation recovery
workflow in GitHub Actions and use **Run workflow**. Open the run summary
for the test result, commit and image ID. Its downloadable evidence includes
the contention test output, the pipeline record and the deployment timeline.

## Follow the drill

| Phase | Operator action and evidence |
| --- | --- |
| Baseline | Make a synthetic booking through the API on loopback. Check its owner and claim ID from PostgreSQL. Keep this reservation as the control. |
| Deploy the fault | Revoke the application role's `INSERT` on `slot_claims` in the lab database. Each subsequent booking probe uses a different existing, unclaimed slot and its own claim ID. |
| Diagnose | Capture the first failed `POST`, its UTC response time and claim ID. Correlate the API log's `InsufficientPrivilege` with that claim and verify the effective privilege. `GET /ready` can still return `200` because its query only reads the parent slot. |
| Recover | Restore `INSERT` to the same role on that table. The next successful probe must return `201 Confirmed` for a fresh claim. Verify the corresponding row and the original control in PostgreSQL. |

The role also serves the worker, so the faulty grant can affect both write
paths. This drill measures recovery of the public-facing API operation. A
`409 SlotTaken` would indicate an occupied fixture and invalidate the
measurement. If the error, image ID or stored row differs from the expected
evidence, investigate the discrepancy before declaring recovery.

The two configuration changes below are performed by the drill's database
operator **only inside its private Compose project**.

```sql
REVOKE INSERT ON slot_claims FROM reservation_app;
GRANT INSERT ON slot_claims TO reservation_app;
```

The [drill runner](./drill.py) probes on a two-second schedule. Subtract the
UTC timestamp of the first failed booking response from the UTC timestamp of
the first confirmed response after the grant is restored. This is the
customer-visible interval observed by the probes. A repair between probes
is observable only on a later sample. Keep the sampling interval with the
result when comparing drills.

## Repeat locally and reset

Use Linux, Git, Python 3 and Docker with Compose supporting `up --wait`.
Start at the repository root on a clean checkout of the revision you intend
to test. The first build needs registry and Python package index access.
The following commands build a candidate from that checkout and run the lab
with the image you just built. The GitHub workflow also runs the #21
contention test before deploying the candidate.

```bash
export SOURCE_REVISION=$(git rev-parse HEAD)
export RESERVATION_IMAGE="reservation-ci:$SOURCE_REVISION"
docker build --label "org.opencontainers.image.revision=$SOURCE_REVISION" \
  -t "$RESERVATION_IMAGE" examples/reference-implementations/small-production-service/reservations
export EXPECTED_IMAGE_ID=$(docker image inspect --format '{{.Id}}' "$RESERVATION_IMAGE")
records=$(mktemp -d)
python3 examples/operational-scenarios/deployment-and-rollback/reservation-recovery/drill.py \
  --output "$records/drill.json"
```

The runner creates a fresh project, selects an available loopback port and
removes its containers, network and volume at the end. To reset and repeat,
run it again with a new output file. Keep the previous JSON to compare runs.
If your Docker daemon has exhausted its address pool, set
`RESERVATION_SUBNET` to an unused private CIDR before starting.

For recovery decisions, see the [deployment rollback runbook](../../../../runbooks/deployment-rollback-and-service-recovery.md).
PostgreSQL documents how grants from multiple sources determine effective
access and how to query it. [REVOKE](https://www.postgresql.org/docs/17/sql-revoke.html)
and [privilege inquiry functions](https://www.postgresql.org/docs/17/functions-info.html#FUNCTIONS-INFO-ACCESS-TABLE).
