# Minecraft Bedrock Marketplace Research - Phase 0 Findings

## Source Index (Phase 0 - Context Gathering)

| # | Source | Type | Signal | Notable Content |
|---|--------|------|--------|-----------------|
| 1 | Microsoft Learn: Minecraft Bedrock Creator Documentation | Official Documentation | ★★★★★ | Complete creator portal with tutorials, references, learning journeys |
| 2 | YouTube: "How to become a Minecraft Marketplace Creator" (Chewboom) | Video Tutorial | ★★★★☆ | 199K views, 4 years old, walks through application process |
| 3 | YouTube: "Minecraft Marketplace Partner: How to ACTUALLY Get Accepted" (Generalist Programmer) | Video Tutorial | ★★★★☆ | 9 min, 2 weeks old, covers 70/30 split, portfolio tips, earnings calculator |
| 4 | YouTube: "The Minecraft Marketplace Partner Program applications are closed" (ASpecificUsername) | Short | ★★★☆☆ | 1.3K views, 1 year old - indicates program may have closed periods |
| 5 | YouTube: "Minecraft is PAYING Creators? (Affiliate Program Explained)" (KYLEBIRK MC) | Video | ★★★★☆ | 8 min, 2 weeks old - NEW affiliate program separate from partner program |
| 6 | HN Comment: mattdesl (2022) | Forum Comment | ★★★★☆ | Confirms Minecoin/Marketplace is official; EULA prohibits selling Minecraft IP outside official marketplace |
| 7 | HN Comment: cruano (2022) | Forum Comment | ★★★☆☆ | Mentions Marketplace + Realms subscription as revenue streams |
| 8 | bedrock.dev | Community Wiki | ★★★☆☆ | Documentation site but marketplace pages return 404 |

## Key Findings (Phase 0 - Unverified, Needs Deep Research)

### Official Documentation
- **Primary Portal**: https://learn.microsoft.com/en-us/minecraft/creator/
- **Learning Journey**: Structured courses from "Getting Started with Add-Ons" → "Learn About Blocks/Entities/Items" → "Changing the Game" → "Get to Know the Tools"
- **Reference Docs**: Scripting APIs, Molang, Commands, Entities, Blocks, Items, Recipes, NPCs, Loot Tables
- **Tools**: Block Wizard, Entity Wizard, Bedrock Editor, VS Code extensions

### Marketplace Partner Program
- **Application Process**: Requires portfolio submission, review by Microsoft/Mojang
- **Revenue Split**: Appears to be 70/30 (creator gets 70%) based on recent video
- **Content Types**: Maps, skins, texture packs, add-ons, worlds
- **Currency**: Minecoins (purchased with real money)
- **Status**: May have open/closed application periods (1-year-old short says "closed")

### New Affiliate Program (2024/2025)
- Separate from Partner Program
- Allows creators to earn commission promoting Marketplace content
- Very recent (2 weeks ago videos)

### EULA/Legal Constraints
- **Critical**: Selling Minecraft IP (mods, skins, merch) outside official Marketplace violates EULA
- All monetization must go through official channels
- Microsoft maintains strict control over IP

### Content Creation Tiers (from Learning Journey)
1. **Resource Packs** - Textures, models, sounds
2. **Behavior Packs** - Game logic, entity behaviors, custom blocks/items
3. **Scripting/API** - JavaScript/TypeScript for advanced logic
4. **Commands/Command Blocks** - In-game logic without code
5. **World Templates** - Pre-built experiences

## Decomposition Strategy (Proposed for Phase 1)

### Aspect-Based Decomposition (Recommended)
1. **Marketplace Economics & Revenue** - Partner earnings, revenue splits, Minecoin economics, top creator case studies
2. **Partner Program Requirements & Application** - Portfolio standards, review process, acceptance rates, timeline
3. **Content Types & Technical Requirements** - Resource vs Behavior packs, scripting limits, file size limits, validation
4. **Official Documentation & Learning Resources** - Microsoft Learn coverage, community tutorials, gap analysis
5. **Audience Building & Marketing** - Discovery algorithms, social media strategies, cross-platform promotion
6. **Legal/IP Constraints & EULA Compliance** - What's allowed, brand guidelines, revenue reporting, taxes
7. **Alternative Paths** - Affiliate program, Realms, external content (YouTube/Twitch), Java edition mods

### Source-Based Decomposition (Alternative)
1. **Official Microsoft/Mojang Sources** - Learn docs, partner portal, blog posts
2. **YouTube Creator Community** - Tutorial channels, income reports, application walkthroughs
3. **Community Wikis/Forums** - bedrock.dev, MCPEDL, Discord communities
4. **Hacker News/Reddit Discussions** - Business model analysis, creator experiences
5. **Indie Game Dev Post-Mortems** - Cross-platform UGC marketplace comparisons

## Numbers Ledger (To Populate in Phase 1)

| Value | Claim | Source | Status |
|-------|-------|--------|--------|
| 70/30 | Revenue split (creator/Microsoft) | YouTube [3] | Needs verification |
| 199K | Views on "How to become Creator" video | YouTube [2] | Verified |
| 4 years | Age of primary tutorial video | YouTube [2] | Verified |
| 2 weeks | Age of newest affiliate program video | YouTube [5] | Verified |
| 1 year | Age of "applications closed" short | YouTube [4] | Verified |

## Research Gaps (To Fill in Deep Research)

1. **Actual revenue data** - No public earnings reports from creators found yet
2. **Application acceptance rate** - No official statistics
3. **Top creator earnings** - No verified figures
4. **Marketplace size** - Total creators, total content pieces, monthly active buyers
5. **Conversion rates** - Impressions → purchases for different content types
6. **Review timeline** - How long from submission to approval/rejection
7. **Portfolio requirements** - Specific quality bars, examples of accepted/rejected portfolios
8. **Content update policy** - Can creators update published content? Revenue impact?
9. **Tax/legal structure** - 1099 vs W2, international creators, Minecoin conversion rates
10. **Affiliate program details** - Commission rates, cookie duration, tracking

## Next Steps

Proceed to Phase 1: Deep Research Reports for each aspect (50-1000 sources each).
Priority order based on user's goal (3-year path to full-time game dev via marketplace):
1. Marketplace Economics & Revenue (most critical for viability assessment)
2. Partner Program Requirements & Application (gatekeeper)
3. Content Types & Technical Requirements (skill building roadmap)
4. Audience Building & Marketing (growth strategy)
5. Legal/IP Constraints (risk mitigation)
6. Official Documentation & Learning Resources (learning path)
7. Alternative Paths (fallback options)