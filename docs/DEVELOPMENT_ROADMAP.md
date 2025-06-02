# Philosophy Pipeline Development Roadmap

## Primary Goal
**Be the first to publish an autonomously generated philosophy paper in a peer-reviewed journal**

Success Metric: Paper deemed "submittable" by philosophy professor standards (not perfect, but journal-ready)

## Strategic Priorities
1. **Speed to Acceptable Quality** > Perfect Quality
2. **Literature Engagement** (biggest current gap)
3. **Prompt Engineering** (quickest wins)
4. **Depth & Sophistication** (minimum viable for submission)

## Phase-Specific Plans

### Phase I: Topic & Literature Discovery
**Status**: Collaborator working on subfield reports approach

**Planned Architecture**:
```
Subfield Reports (cached, ~3 month refresh)
├── accuracy_first_epistemology.pdf
├── feminist_philosophy_of_science.pdf
├── virtue_epistemology.pdf
└── [other subfields]
    ↓
Topic Selection (informed by landscape)
    ↓
Targeted Paper Search (PhilPapers/Semantic Scholar)
    ↓
Two-tier Literature:
├── Deep Engagement Papers (3-5 for substantial analysis)
└── Context Papers (10-15 for citations/landscape)
```

**Open Questions**:
- Automated PDF retrieval vs. manual
- `read` tool implementation timing
- Integration with existing Phase I.2

### Phase II: Framework & Content Development
**Priority Improvements**:

1. **Phase II.1 (PDF Reading)** - HIGHEST PRIORITY
   - Implement structured extraction with page numbers
   - Add quotation harvesting
   - Create argument mapping
   - Track specific terminology

2. **Phase II.3 (Key Moves)** - SECOND PRIORITY
   - Add philosophical stakes requirements
   - Implement objection anticipation
   - Require dialectical positioning
   - Ensure conceptual depth

### Phase III: Writing & Polish
**Focus**: Good enough for submission, not perfection

Key improvements:
- Better section-to-section flow
- Reduce repetition
- Ensure citations are plausible (even if not perfect)

## Implementation Timeline

### Week 1: Planning & Prompt Engineering Prep
- [ ] Finalize roadmap documents
- [ ] Create prompt templates for Phase II.1
- [ ] Design quality rubric for "submittable" threshold
- [ ] Set up output archiving system

### Week 2-3: Phase II.1 Enhancement
- [ ] Implement enhanced PDF reading prompts
- [ ] Add structured extraction
- [ ] Test with sample papers
- [ ] Measure improvement in literature engagement

### Week 4-5: Phase II.3 Enhancement  
- [ ] Add depth requirements to key moves
- [ ] Implement dialectical positioning
- [ ] Test philosophical sophistication

### Week 6-7: Full Pipeline Testing
- [ ] Run complete pipelines with improvements
- [ ] Assess against "submittable" criteria
- [ ] Identify remaining gaps

### Week 8+: Iterate to Submission Quality
- [ ] Focus on biggest remaining gaps
- [ ] Polish as needed for submission

## Quality Rubric for "Submittable"

**Must Have**:
- [ ] Clear, novel thesis
- [ ] Engagement with 10+ relevant sources
- [ ] Valid argumentative structure
- [ ] Addresses obvious objections
- [ ] Professional writing quality
- [ ] ~3000-4000 words

**Nice to Have** (can improve post-submission):
- [ ] Perfect citations with page numbers
- [ ] Deep engagement with cutting-edge debates
- [ ] Highly original philosophical move
- [ ] Beautiful prose

## Risk Mitigation
- Focus on less technical topics (avoid formal logic, complex metaphysics)
- Target journals that value clarity and novel perspectives
- Have backup topics ready if current approach stalls 