# Philosophy Pipeline Development Roadmap

## Current State
- ✅ Complete end-to-end pipeline generating full papers (~145 minutes)
- ✅ Analysis journal integration with 45% word reduction
- ✅ Development/Critique/Refinement cycles with philosophical rigor
- ✅ Hájek heuristics integrated for catching philosophical errors
- ✅ Anti-RLHF prompts for bolder philosophical claims
- ✅ Pattern database with 66 moves from 10 Analysis papers
- ⚠️ Papers improving but still need more dialectical depth
- ⚠️ Temperature optimization pending systematic testing

## Priority 1: Low-Hanging Fruit (1-2 Days) ✅ MOSTLY COMPLETE

### 1.1 Integrate Philosophical Heuristics into Critics ✅ COMPLETED
- Add Hájek-style heuristics to all critic prompts
- Focus on: extreme case testing, self-undermining detection, counterexample generation
- **Impact**: Catch "dumbass arguments" like backward-looking epistemic responsibility
- **Effort**: 2 hours
- **STATUS**: COMPLETED - Integrated across Phase II.1-4 and III.1-2
- **Results**: Critics now systematically test for boundary cases, self-defeat, hidden assumptions

### 1.2 Temperature Optimization ⏳ PENDING
- Critics: 0.0-0.1 (maximum rigor)
- Development: 0.4-0.6 (balanced creativity)  
- Examples: 0.7-0.8 (creative scenarios)
- **Impact**: Better philosophical precision
- **Effort**: 1 hour setup + testing
- **STATUS**: Requires systematic hyperparameter sweep, not just manual settings

### 1.3 Quick Pattern Extraction ✅ COMPLETED
- Extract from Analysis papers:
  - ✅ 66 philosophical moves extracted from 10 papers
  - ✅ Categorized by type (offensive, defensive, constructive, meta)
  - ✅ Curated examples database integrated
- Store as JSON for immediate few-shot capability
- **Impact**: Instant Analysis style improvement
- **Effort**: 4 hours
- **STATUS**: COMPLETED - Extracted, curated, and injected into Phase II.2, II.3, and II.4

### 1.4 Anti-RLHF Enhancements ✅ COMPLETED
- Development workers: Add "philosophical courage" prompts
- Refinement workers: "Preserve productive tensions"  
- Writers: "Take a stand" instructions
- **Impact**: Bolder, clearer philosophical arguments
- **Effort**: 2 hours
- **STATUS**: COMPLETED - Integrated across all Phase II & III workers
- **Results**: Papers now use "I argue" instead of "explores", take clear positions

### 1.5 Bug Fixes & Prompt Hygiene ✅ COMPLETED (NEW)
- Fixed Phase II.3 2-move limitation bug (now processes all 5 moves)
- Standardized XML tags across all prompts
- Fixed contradictory requirements (abstract length, quote counts)
- Added navigation aids for complex prompts
- **Impact**: More reliable pipeline, easier model comprehension
- **Effort**: 3 hours
- **STATUS**: COMPLETED

## Priority 2: High-Impact Structural Changes (1 Week)

### 2.1 Dialectical Development Phase (New Phase II.3.5)
- Insert between Key Moves and Detailed Outline
- For each key move: Generate 3 objections → responses → counter-responses
- Creates philosophical "texture" missing from current papers
- **Impact**: Major improvement in philosophical sophistication
- **Effort**: 3-4 days

### 2.2 Referee Simulation (Phase III.3)
- Add referee report generation after paper completion
- Different mindset from "critic" - catches different issues
- Explicit Accept/Minor/Major/Reject recommendation
- **Impact**: Identifies publication barriers
- **Effort**: 1 day

### 2.3 Philosophical Health Checks
- Between phases: Check universal claims, causal mechanisms, example quality
- Prevent embarrassing errors before they propagate
- **Impact**: Consistent quality control
- **Effort**: 1 day

## Priority 3: Comprehensive Enhancements (2+ Weeks)

### 3.1 Full Pattern Database Development
- Systematic extraction from 20+ Analysis papers
- Categorized by: openings, distinctions, dialectical moves, transitions
- ML-powered retrieval based on topic
- **Impact**: Transform from "generic philosophy" to "Analysis philosophy"
- **Effort**: 2 weeks

### 3.2 Multi-Model Strategy
- Novelty detection: o1/o3 (best at meta-reasoning)
- Deep philosophy: Claude Opus
- Efficiency: Sonnet/Haiku based on task
- **Impact**: Leverage model strengths
- **Effort**: 1 week

### 3.3 Novelty Detection System
- Database of recent philosophy papers' theses
- Systematic comparison framework
- "Is this genuinely new?" evaluation
- **Impact**: Essential for publication
- **Effort**: 1 week

## Quick Implementation Wins

### Tomorrow's Meeting Priorities
1. **Heuristics Integration** - Biggest bang for buck
2. **Quick Pattern Extraction** - Enables immediate few-shot
3. **Anti-RLHF Prompts** - Unlocks bolder philosophy
4. **Referee Simulation** - New perspective on quality

### Division of Labor
- You: Pattern extraction, heuristics integration, RLHF optimization
- Collaborator: Citation improvements (already working on)
- Shared: Testing protocol, quality metrics

## Success Metrics

### Quantitative
- Objection anticipation rate: >80%
- Conceptual precision: All key terms distinguished
- Dialectical depth: 3+ rounds of objection-response
- Example density: 1 per 400 words

### Qualitative  
- "Philosophical texture" - Reads like real philosophy
- "Referee ready" - Anticipates likely criticisms
- "Analysis voice" - Conversational rigor throughout
- "Bold claims" - Takes philosophical risks

## Immediate Next Steps

### 1. Test Philosophical Moves Injection
- Run Phase II.2 & II.3 with injected examples
- Compare outputs to see if moves patterns appear
- Check if abstract framing improves
- Verify key moves show dialectical patterns

### 2. PDF → TXT Migration Decision
- **Option A**: Keep PDFs for now (stability)
- **Option B**: Switch to TXT immediately (3x context efficiency)
- **Recommendation**: Test current improvements first, then migrate

### 3. Expand Move Injections (If Tests Succeed)
- Add moves to Phase II.4 (outline development)
- Add examples to Phase III.1 (section writing)
- Add extreme cases to more critics

## Concrete First Steps (Do Today)

### A. Heuristics Quick Test
1. Edit `src/phases/phase_two/stages/stage_three/prompts/critic/critic_prompts.py`
2. Add to MoveCriticPrompts: 
   ```
   For EACH major claim:
   - Apply extreme case test: What happens at the boundary?
   - Check self-undermining: Does this claim defeat itself?
   - Generate obvious counterexample a grad student would raise
   ```
3. Run one paper generation and compare critique quality

### B. Pattern Extraction Pilot
1. Take 2 Analysis papers from `analysis_cache/extracted_texts/`
2. Extract:
   - First 2 paragraphs (opening patterns)
   - One clean objection→response→counter-response sequence
   - One conceptual distinction with its introduction
3. Create `analysis_patterns_v1.json` as proof of concept

### C. Temperature Quick Fix
1. Edit `config/conceptual_config.yaml`
2. Set all critic temperatures to 0.1
3. Set example generation temps to 0.7
4. Test if critics become more rigorous

## Proof of Concept Test

**Before Meeting**: Generate 2 papers
1. One with current system (baseline)
2. One with just heuristics + temperature changes

**Compare**:
- Do critics catch more philosophical errors?
- Are the arguments bolder?
- Is the philosophical texture richer?

**Success Indicator**: If the second paper shows noticeable improvement with just 2-3 hours of work, the full roadmap is validated.

## Risk Factors & Mitigation

1. **Over-engineering**: Start small, test, then expand
2. **Model costs**: Test improvements on single papers first
3. **Integration complexity**: Keep changes modular
4. **Quality regression**: Always compare to baseline

## Meeting Talking Points

1. **The Core Problem**: We generate *competent* philosophy, not *compelling* philosophy
2. **The Key Insight**: Need philosophical thinking tools, not just writing instructions
3. **The Quick Win**: 2 days of work could yield dramatic improvements
4. **The Vision**: 70% publication probability is achievable with systematic improvements

## Key Insight
**We need philosophical thinking tools, not just writing instructions.** The pipeline should teach LLMs to think like philosophers, not just write like them.

## Next Steps
1. Implement heuristics in critic prompts (TODAY)
2. Run 5-paper comparison test
3. Extract quick patterns from Analysis papers
4. Design dialectical development phase
5. Test referee simulation on current output

## Expected Timeline to Publishable Quality
- With Priority 1 only: 20% → 35% publication probability
- With Priority 1+2: 35% → 50% publication probability  
- With all priorities: 50% → 70% publication probability

The path to publication is through philosophical rigor, not just clear writing. 