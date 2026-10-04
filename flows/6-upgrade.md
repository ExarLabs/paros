# Flow 6: Upgrade

The repository is updated from time to time: a new principle, a refined one, a better kit. An update is **advice**, never an overwrite.

## Steps

1. The person updates the repository (`git pull`).
2. Read the reference version recorded in the vault: `PAROS/ADOPTION.md`, field `reference_version`.
3. Read the `CHANGELOG.md` entries newer than that.
4. For every change, decide whether it concerns this person:
   - **new principle:** a new checklist item (`to adopt`, `later` or `not needed`);
   - **refined principle:** if already adopted, check whether their version needs a touch; if marked `adapted`, respect their decision;
   - **new or improved kit:** only suggest it if they use that kit or would need it.
5. Write the suggestions into `ADOPTION.md` under a new section "Upgrade to vX.Y.Z", show them, and work through them one by one like in adoption.
6. Optionally run the diagnosis again to show what moved.
7. Update `reference_version`.

## Never

- Overwrite the person's own adaptations because the reference says otherwise.
- Copy anything from the repository automatically.
