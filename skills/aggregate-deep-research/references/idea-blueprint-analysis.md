# Idea Blueprint Analysis — Classification Map & Analysis Templates

Full reference for Phase 5 (Deep-Dive Blueprint Analysis) of the aggregate-deep-research pipeline.

## Two-Pass Category Classifier

### Pass 1: Long/Multi-Word Phrases (substring match — safe)

These phrases are unique enough to never false-match. Checked with simple `kw in name_lower`.

```python
long_phrases = [
    ('utility', ['qr', 'password', 'vpn', 'converter', 'beautif', 'minif', 'optimizer',
                 'license', 'svg', 'isbn', 'barcode', 'emoji', 'schema', 'wcag',
                 'font', 'url builder', 'text diff', 'diff viewer',
                 'whats my ip', 'my ip', 'will my pc']),
    ('finance', ['receipt', 'split', 'bill', 'invoice', 'spreadsheet', 'expense',
                  'bookkeep', 'tax', 'subscription', 'credit', 'overpay',
                  'storefront', 'what if i', 'am i overpay', 'am i being ripped']),
    ('time', ['calendar', 'timezone', 'planner', 'countdown',
              'flight', 'day until', 'days until', 'how many days']),
    ('dev', ['status page', 'uptime', 'changelog', 'screenshot feedback',
             'link-in-bio', 'readme', 'github', 'portfolio page from',
             'regex', 'deploy', 'lint', 'domain name',
             'side-by-side', 'what i learned', 'side project progress',
             'deploy to prod', 'coding challenge',
             'open source alternative', 'this day in history']),
    ('ai', ['phishing', 'bias checker', 'fix my resume', 'highlight reel',
            'content repurpose', 'ai meeting', 'ai inventory']),
    ('social', ['matchmaker', 'marketplace', 'hyperlocal', 'neighbor',
                'barter', 'volunteer', 'feature voting', 'community directory',
                'postcard', 'penpal', 'bulletin',
                'pet care', 'ride sharing', 'help network']),
    ('health', ['symptom', 'elder', 'emergency', 'allerg',
                'baby', 'diaper', 'feeding', 'check-in',
                'doctor', 'meds', 'medication', 'pollen',
                'whats for dinner', 'recipe', 'plant watering',
                'care reminder', 'what should i cook']),
    ('home', ['roommate', 'inventory', 'maintenance', 'maintain',
              'packing list', 'packing', 'parking', 'delivery photo',
              'fridge', 'grocery', 'family calendar',
              'party planner', 'chore wheel', 'chore ',
              'did i take', 'when did i last']),
    ('learn', ['tutorial', 'portfolio page', 'resume', 'ats ',
               'what i learned']),
]
```

### Pass 2: Short Keywords with Word Boundaries (regex)

These would false-match as substrings, so wrap in `\b...\b`:

```python
import re
word_patterns = [
    ('utility', [r'\bspeed\b', r'\bcolor\b', r'\bcode\b', r'\butm\b', r'\bjson\b', r'\byaml\b', r'\btoml\b', r'\burl\b']),
    ('finance', [r'\brent\b', r'\bcost\b', r'\bprice\b', r'\bpay\b']),
    ('time', [r'\btime\b', r'\bwhen\b', r'\bdate\b', r'\bday\b', r'\bhour\b']),
    ('dev', [r'\bapi\b', r'\bbadge\b', r'\bformat\b', r'\bportfolio\b']),
    ('ai', [r'\bai\b', r'\bgenerator\b', r'\bscore\b', r'\bfix\b', r'\bsuggest\b', r'\bhighlight\b', r'\brepurpose\b']),
    ('social', [r'\bsocial\b', r'\bshare\b', r'\bgroup\b', r'\bvote\b', r'\bpoll\b', r'\bnetwork\b', r'\bcommunity\b', r'\bdirectory\b', r'\bride\b', r'\bbrand\b', r'\bsponsor\b', r'\blocal\b']),
    ('health', [r'\bhealth\b', r'\bfood\b', r'\bdiet\b', r'\bmeal\b', r'\bplant\b', r'\bgarden\b', r'\bfever\b', r'\bsick\b']),
    ('home', [r'\bhome\b', r'\bhouse\b', r'\bcar\b', r'\btool\b', r'\bdelivery\b']),
    ('learn', [r'\blearn\b', r'\bcourse\b', r'\bjob\b', r'\bcoding\b']),
]
```

### Return value

```python
for cat, kws in long_phrases:
    for kw in kws:
        if kw in n:      # Pass 1: substring match
            return cat
for cat, pats in word_patterns:
    for pat in pats:
        if re.search(pat, n):   # Pass 2: word-boundary regex
            return cat
return 'general'
```

## Analysis Templates by Category

Each template covers three dimensions for `[MY ANALYSIS]`:

| # | Dimension | What to address |
|---|-----------|-----------------|
| 1 | **User Experience** | Interaction model, friction reduction, visual priorities |
| 2 | **Monetization** | Revenue model, pricing strategy, free vs paid tiers |
| 3 | **Differentiation** | Moat, competitive gap, why existing solutions fail |

### utility
> **User Experience:** Single-purpose utility — every ms of load and every pixel of chrome hurts adoption. Input to result, nothing in between. Privacy-first, PWA-cached, no ads.
> **Monetization:** Open-source core, pro tier with batch/API/white-label.
> **Differentiation:** The gap is single-minded focus. Existing tools cram features; this does one thing perfectly. Encode input in URL hash for zero-infrastructure sharing.

### finance
> **User Experience:** Minimize keystrokes. Photo upload as primary input, auto-detection, manual override. Mobile-first PWA with offline support is non-negotiable.
> **Monetization:** Freemium with monthly limit. Pro with unlimited scanning, CSV export, accounting integration at $5-10/mo.
> **Differentiation:** Local-first (IndexedDB, export anytime) is a genuine advantage. [SOURCE] Key Theme: privacy as competitive moat.

### time
> **User Experience:** Extreme focus — one interaction, one output. Minimal UI for one specific problem.
> **Monetization:** Link-viral mechanics drive free marketing. Pro: custom domains, recurring events, view analytics.
> **Differentiation:** Speed beats features. Under 1s load, under 3 clicks to result beats every bloated alternative.

### dev
> **User Experience:** Dev tools must be fast, keyboard-navigable, no JS bloat. Dark mode mandatory. Devs want tools that feel native.
> **Monetization:** Open-source for audience-building, hosted paid for team features/SSO/audit.
> **Differentiation:** The winning dev tool 'just works' with zero configuration. Speed over features.

### ai
> **User Experience:** AI should be invisible — input, output, no 'AI thinking...' states. Progress indicators yes, but LLM calls should feel instant.
> **Monetization:** Credit-based (10 free credits/month, then pay-per-use). Avoids subscription fatigue for occasional use.
> **Differentiation:** Thin AI wrappers have no moat. Differentiate with structured output, validated forms, domain-specific prompt chains — not generic ChatGPT wrappers. The moat is in the workflow, not the model.

### social
> **User Experience:** Zero-friction onboarding. No-account approach is #1 adoption killer. Shareable links as primary access, not accounts.
> **Monetization:** Charge one side (businesses/power users), keep the other free. Flat fee beats percentage for low-trust marketplaces.
> **Differentiation:** Start hyperlocal, go deep before broad. Local works but is underbuilt.

### health
> **User Experience:** Simple enough for stressed/tired/distracted users. Data privacy is table stakes — explain why data stays on-device.
> **Monetization:** Family plans ($5/mo for up to 6). Free basic tracking, paid reports/doctor-sharing/export.
> **Differentiation:** Gap is practical daily management — not clinical (too complex for users) and not fitness (too casual for real health needs).

### home
> **User Experience:** Solve real-life friction that existing apps ignore. Must work offline, must be shareable with non-tech-savvy family members.
> **Monetization:** Household pricing ($3-5/mo shared). Free for one household, paid for multiple properties or team access.
> **Differentiation:** Existing home management apps are either toys (gamified but useless) or construction-grade (overkill for families).

### learn
> **User Experience:** Learners need guided paths, not blank slates. Templates and examples as starting points. Progress tracking and streaks motivate continued use.
> **Monetization:** Free tier with limited content. Pro with structured curriculum, personalized feedback, certification.
> **Differentiation:** Most learning platforms are content-first (passive). This should be project-first (active).

### general (fallback)
> **User Experience:** [SOURCE] validates real frustration. UX priority: reduce steps to completion. Every extra field causes drop-off.
> **Monetization:** Free individual, team pricing for shared features.
> **Differentiation:** Competitors are either overly complex (enterprise) or abandoned (side projects). The gap is a maintained, simple, modern alternative.

## Source Extraction Regex

Parse report-01's markdown for detailed idea context:

```python
# Extract structured blocks (each starts with ### TIER.SEQ)
idea_blocks = re.findall(r'(### \d+\.[^#]*?)(?=\n### |\n## |\Z)', markdown_text, re.DOTALL)

# Within each block, extract fields:
for field_name, label in [
    ('problem', 'Problem'),
    ('solution', 'Solution'),
    ('why_unsolved', 'Why unsolved'),
    ('stack', 'Stack'),
]:
    match = re.search(r'\*\*'+label+r':\*\*(.*?)(?:\n\*\*|\Z)', block, re.DOTALL)
    if match:
        result[field_name] = match.group(1).strip()
```

## Report Structure Template

```markdown
### #{num}: {name}
**Effort:** {effort}
**Category:** {category}
**Sources:** {sources}

#### Intent & Origin [SOURCE]
Core frustration or identified need.
Validation approach: {validation}

#### Design Objective [SOURCE]
Original design brief or proposed solution.
Why existing solutions miss the mark.
Tech stack suggestion.

#### My Analysis [MY ANALYSIS]
**User Experience:** {UX strategy}
**Monetization:** {revenue model}
**Differentiation:** {competitive gap}
```

## Appendix Template (10 Design Principles)

Close every blueprint report with these principles, tailored to the subject:

1. **Start with the output, not the input.** Design the result first, then work backward.
2. **One screen, one job.** If it needs nav/tabs, it's probably two apps.
3. **Offline-first is a competitive moat.** PWA + local-first > cloud-only.
4. **URL hash for zero-infrastructure sharing.** Store state in URL fragments.
5. **Privacy as a feature.** "We never see your data" as the headline.
6. **AI is a component, not a product.** The product is the workflow.
7. **Build for the sharable moment.** Every output markets itself.
8. **The best time to monetize is never.** Audience first, monetization second.
9. **Hyperlocal before global.** Prove in one neighborhood, then expand.
10. **Document your build publicly.** Writing about the build IS the marketing.
