# HumanFrame Robotics public website

A static, multi-page website for HumanFrame Robotics and Alp, its developing social research robot for universities, educators and human-robot interaction researchers. The runtime, SDK and application Platform explain the software foundation behind the robot. First-generation mobility is planned and undemonstrated; future humanoids are a separate long-term direction.

The current implementation follows the user-authorized `HumanFrame_Website_Redesign_Package.zip`: warm ivory and sage, product-led editorial layouts, genuine supplied team portraits and a dedicated reminiscence research case study. No production deployment has been made.

## Preview and validate

From this repository directory:

```sh
python3 scripts/preview.py
```

Open http://127.0.0.1:8080/. No installation or build step is required. Stop any
existing preview server with Ctrl+C before restarting it.

If your terminal is in the parent workspace containing this website folder, run:

```sh
python3 humanframe-website/scripts/preview.py
```

The preview script always serves the directory containing the site's `index.html`,
even when started from another directory. Serving the parent workspace with a plain
`python3 -m http.server` makes root-relative links such as `/team/` return 404.

```sh
python3 scripts/validate_site.py
node --check assets/js/site.js
git diff --check
```

The Python validator uses only the standard library. It checks routes, fragments, assets, image dimensions, navigation, SEO/social metadata, sitemap, static-host policy, the inquiry form, team labels and the illustrative reminiscence grid. Browser review is still required for visual changes.

## Routes and hosting

Main destinations are `/`, `/robot/`, `/features/`, `/research/`, `/framework/`, `/why-humanframe/`, `/applications/reminiscence/`, `/team/` and `/contact/`. Existing `/alp/`, `/technology/`, `/developers/`, `/platform/` and `/about/` remain functional pages. `404.html` provides the custom error page.

Serve this directory as the static site root and preserve directory indexes. For the existing Vercel project, retain its domain/Git integration, use the **Other** framework preset and an empty build command. `vercel.json` supplies security/cache headers equivalent to `_headers`, with native file routing and no catch-all rewrite. These files do not deploy anything by themselves. A push or deployment requires explicit approval.

## Content and maintenance

- The selected product visuals are labelled design concepts, not photographs of completed hardware. Team portraits and development CAD come from the supplied package. See [asset provenance](assets/media/ASSET_SOURCES.md).
- Existing HumanFrame branding, favicon, local Lato fonts and the Platform development screenshot are retained. Older robot artwork remains unused.
- The public inbox is `hello@humanframerobotics.com`. The contact page validates details and prepares a plain-text `mailto:` draft. Visitors review and send it in their own email app. There is no POST endpoint, backend storage or automatic sending; a direct email fallback works without JavaScript.
- Native disclosure menus, responsive layouts, visible keyboard focus and reduced-motion preferences are supported. Headings, buttons, architecture diagrams and the illustrative research interface are HTML.
- Shared CSS/JavaScript URLs use content-hash query versions. Update the relevant version across all HTML pages after changing a shared asset.
- The SDK is in development, with no announced public release or download. Pricing and availability are not announced. The spring 2027 research-ready pilot is a qualified development target.
- The operational Platform, robot runtime, authentication and deployment infrastructure are separate from this website and were not modified.

See [REDESIGN_NOTES.md](REDESIGN_NOTES.md) for the full changed-file list, verification status and publication review items.
