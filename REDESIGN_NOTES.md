# Website redesign handoff

Implemented locally on `codex/alp-website-redesign`. No commit, push or production deployment was performed.

## Scope and starting point

All 38 original website files were inspected. The original static export matched `WadAdrian/humanframe-website` at `main` commit `948e2bcba98fc7c75ee79820c9f1215a0fdb9bf6` byte for byte. Existing routes, branding, local Lato fonts, favicon and the Platform screenshot were preserved. No backend, robot runtime or operational deployment infrastructure was changed.

The user explicitly authorized `HumanFrame_Website_Redesign_Package.zip` as the revised controlling brief. The site now follows its research-first product positioning and ivory/sage editorial direction, replacing the earlier dark design. Alp is the developing social research robot; its software makes custom interaction research possible. More capable humanoid embodiments remain a separate future vision.

## Implemented experience

The homepage uses the selected landscape product concept, concise HTML copy and three substantial feature compositions. It introduces interaction, research and the integrated software foundation, with genuine supplied development CAD, a reminiscence application teaser and collaboration links. The runtime/SDK/Platform support the robot story.

Dedicated Robot, Features, Research, Framework and Why HumanFrame pages explain the intended product, current prototype foundations and planned capabilities. A native HTML architecture shows the relationship between applications, SDK, runtime and robot. Mobility is explicitly planned and undemonstrated. The first research-ready pilot target is the end of the 2026–27 academic year (spring 2027), subject to development and validation, with no guaranteed launch or delivery date.

The Team page contains exactly four supplied portraits, names and roles, with restrained biographies and a fuller account of Adrian's cross-disciplinary work. The Reminiscence page distinguishes the earlier Pepper/RoboCare research prototype from HumanFrame's unfinished adaptation. Its nine-prompt tablet illustration and sample conversation are native HTML, clearly illustrative and contain no participant records. Research questions are presented without clinical efficacy or privacy-policy claims.

The header uses native disclosure menus for Technology, Applications and About, with keyboard/touch navigation and a mobile menu. All existing pages remain functional and discoverable in the footer. Public pages have distinct titles/descriptions, canonical and social metadata; the 404 is marked noindex. Shared assets use content-hash query versions. Vercel retains native static routing and equivalent security/cache headers.

### Contact

The approved public inbox is `humanframerobotics@gmail.com`. The client-side inquiry helper validates required details, displays a plain-text preview and prepares an encoded `mailto:` draft. It never sends a message or submits to a backend; the visitor sends it from their email app. Editing/resetting clears a stale draft. Research links preselect the collaboration topic. The direct email fallback remains available without JavaScript.

### Media

Nine selected WebPs from the ZIP were copied byte-for-byte into `assets/media/product/`, `engineering/` and `team/`, totaling **367,852 bytes (about 359 KiB)**. No new images were generated for this implementation. Product renders are labelled concepts; CAD is labelled development work; the existing dashboard is labelled test/example data. CSS hides only the supplied portrait's empty bottom border while keeping the complete robot visible; the source file is unchanged.

Earlier artwork and six showcase crops remain unused. They are preserved as existing work, with no public HTML, stylesheet or social-image references. [ASSET_SOURCES.md](assets/media/ASSET_SOURCES.md) records provenance and the source-review limits.

## Changed files

Modified existing files:

- `index.html`
- `alp/index.html`
- `technology/index.html`
- `platform/index.html`
- `developers/index.html`
- `about/index.html`
- `contact/index.html`
- `404.html`
- `assets/css/tokens.css`
- `assets/css/base.css`
- `assets/css/public.css`
- `assets/js/site.js`
- `sitemap.xml`
- `README.md`

Added pages:

- `robot/index.html`
- `features/index.html`
- `research/index.html`
- `framework/index.html`
- `why-humanframe/index.html`
- `applications/reminiscence/index.html`
- `team/index.html`

Added selected media and provenance:

- `assets/media/product/alp_hero_soft_studio.webp`
- `assets/media/product/alp_portrait_soft_studio.webp`
- `assets/media/product/alp_expression_closeup.webp`
- `assets/media/product/alp_mobility_concept_detail.webp`
- `assets/media/engineering/robot_head_cad_work_in_progress.webp`
- `assets/media/team/adrian-wadhwa.webp`
- `assets/media/team/jacob-camoin.webp`
- `assets/media/team/rudy-arsenault.webp`
- `assets/media/team/theron-boozer.webp`
- `assets/media/ASSET_SOURCES.md`

Added during the earlier revision and now unused:

- `assets/media/research/alp_hero_portrait.webp`
- `assets/media/research/alp_turnaround.webp`
- `assets/media/research/alp_face_detail.webp`
- `assets/media/research/alp_touchscreen_detail.webp`
- `assets/media/research/alp_mobility_detail.webp`
- `assets/media/research/alp_research_lab.webp`

Added supporting files:

- `vercel.json` — static hosting and security/cache policy.
- `scripts/validate_site.py` — dependency-free validation.
- `REDESIGN_NOTES.md` — this handoff.

Removed:

- `assets/js/init.js` — early content hiding was consolidated into progressive enhancement in `site.js`; no HTML references remain.

No packages, build dependencies or framework migration were introduced.

## Verification status

- Static validation passes: **15 HTML pages, 3 stylesheets, 20 image elements and 636 references**. Checks cover all 14 public routes plus the 404, local links/fragments/assets, dimensions, navigation, metadata, sitemap, static-host policy, team labels, the native nine-prompt illustration and inquiry form. Superseded artwork references and public implementation jargon are rejected.
- `node --check assets/js/site.js` and `git diff --check` pass.
- Browser layout checks pass for all 15 pages at 1440, 390 and 320 CSS pixels, with no horizontal overflow or broken loaded images. At 768 pixels, Home, Robot, Framework, Team, Reminiscence and Contact also pass.
- Keyboard checks pass for the desktop Technology disclosure and its Features/Framework links. Mobile Menu and Applications open with Enter; Escape closes the disclosure, then the menu, restoring focus.
- Final inquiry checks pass required-field validation, research-topic prefill, encoded recipient/subject/body, safe plain-text preview, clearing after edits, and reset. No email app was opened and no test email was sent.
- The final tested Contact tab has no warning/error console messages. Four core text/background contrast pairs meet 4.5:1, including muted text on sage at 4.57:1. Shared asset hash versions are current on all 15 pages.
- The final source content audit found no unsupported sales, pricing, customer, clinical, privacy or autonomy claims, public implementation jargon, placeholder destinations, old artwork references, bright-blue UI or numbered roadmap badges.
- Static routing and header parity are checked locally. Live Vercel behavior requires an approved deployment to verify end to end.

Current preview screenshots are outside the repository in `../deliverables/website-package-redesign/`: `home-desktop.png`, `home-mobile.png`, `team-desktop.png`, `team-mobile.png`, `reminiscence-desktop.png` and `reminiscence-mobile.png`. The final layout and interaction QA record is `layout-checks.json` in the same folder. `home-desktop-hero.png` provides a compact homepage preview. Earlier screenshot folders depict superseded revisions.

## Publication review

There are no unfinished placeholder destinations, fake SDK downloads, dummy submission endpoints or promised product availability. The neutral memory prompts and sample dialogue are intentional illustrations, not missing production content. There is no public SDK release, pricing, checkout or functioning server-side contact form implied.

The adjacent CM5 snapshot and related source were inspected read-only to ground narrow claims about local deployment, execution and camera/audio capture prototypes. Hardware tests were **not rerun** for the website work. The complete research robot and integrated web-to-robot workflow remain in development.

Founder review is still required for:

- The four portrait identities, names, roles, biographies and ongoing studies.
- The CAD's provenance. The supplied package attributes it and the portraits to `Demo Day V.0(1).pdf`, pages 8 and 10; that original deck was not inspected in this task.
- The precise Pepper/RoboCare prototype history and current HumanFrame adaptation status.
- The freshness of recorded hardware/software prototype results and current integrated-system status.
- The qualified spring 2027 pilot target and whether it remains appropriate to state publicly.
- The existing dashboard's suitability for publication and whether the supplied inbox is monitored.

No institutional endorsement, customer adoption, medical outcomes, quantified affordability, autonomous navigation, safety certification or shipping commitment is claimed.
