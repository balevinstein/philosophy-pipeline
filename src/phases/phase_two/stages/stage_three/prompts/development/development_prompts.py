from typing import Dict, Any, Optional, List


class MoveDevelopmentPrompts:
    """Prompts for key move development in Phase II.3."""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing key argumentative moves. Your role is to create complete, publication-ready philosophical content that advances the paper's thesis. You must produce concrete arguments, examples, and literature integration - not meta-commentary. Your output will be used directly in an automated paper generation pipeline."""

        self.curated_examples_database = """
<philosophical_examples_from_analysis>
<examples>
<example>
<paper_title>Anonymity and Non-Identity Cases</paper_title>
<type>thought_experiment</type>
<purpose>Introduces the standard non-identity case to motivate the Non-Identity Principle by testing our intuitions about replacing one person with another</purpose>
<context>Used to establish the foundation for the Non-Identity Principle by presenting a clear case where we must choose between bringing different people into existence</context>
<text>Consider a standard non-identity case, in which one must choose between bringing Eve into existence, with a better life, or instead bringing Adam into existence, with a worse (but still good) life. Imagine that nobody else is affected by this choice, and that there are no other potentially morally relevant differences at play: Adam and Eve are equally deserving, no impersonally valuable things are affected, and so on.</text>
</example>

<example>
<paper_title>Anonymity and Non-Identity Cases</paper_title>
<type>counterexample</type>
<purpose>Shows the absurd consequences of rejecting the Non-Identity Principle by demonstrating how it leads to counterintuitive evaluations when combined with plausible assumptions</purpose>
<context>Used to argue against rejecting the Non-Identity Principle by showing what would follow if we combined its rejection with Same-Person Anonymity</context>
<text>|     | Adam | Steve | Eve |
|-----|------|-------|-----|
| A   | 60   | 80    | X   |
| B   | 60   | X     | 40  |
| C   | 80   | 60    | X   |

Intuitively, C is better than B. Same-Person Anonymity implies that A and C are equally good. Transitivity then implies that A is better than B, in line with the Non-Identity Principle. If we want to reject this instance of the Non-Identity Principle, it thus looks like we have to say that C is not better than B, despite appearances. But compare B and C directly. We can imagine going from C to B by making two changes. First, we make Adam worse off by twenty units of wellbeing. Second, we replace Steve with the worse-off Eve.</text>
</example>

<example>
<paper_title>Anonymity and Non-Identity Cases</paper_title>
<type>thought_experiment</type>
<purpose>Provides a large-scale counterexample to demonstrate the absurdity of rejecting the Non-Identity Principle when applied to real-world population sizes</purpose>
<context>Used to strengthen the argument for the Non-Identity Principle by showing its rejection leads to obviously wrong conclusions about global population changes</context>
<text>Consider two possible futures. In the first future, the present seven billion inhabitants of Earth will each enjoy 80 units of wellbeing, and there will exist seven billion future individuals, each with 60 units of wellbeing. In the second future, the present inhabitants will instead have 60 units of wellbeing, while seven billion future individuals, who are non-identical to the individuals existing in the first future, will have only 40 units of wellbeing. If we suppose that it does not make the world better to replace any number of lives at level 40 by the same number of lives at level 80, an argument exactly analogous to that of the preceding paragraph shows that, given Same-Person Anonymity and Transitivity, the second future is not worse than the first.</text>
</example>

<example>
<paper_title>Can a risk of harm itself be a harm?</paper_title>
<type>thought_experiment</type>
<purpose>Tests whether subjective risks can constitute harms by creating a case where there is subjective risk but no objective possibility of harm</purpose>
<context>Used to support the Interference Objection against subjective accounts of risk harm</context>
<text>Russian Roulette Aggressor: Completely unbeknown to Adam, who is enjoying the weather on a park bench, Beth is aiming a six-shooter at him with the intention to kill him. Beth loads a single bullet into the cylinder. However, Beth in fact loads a blank, but does not realize this. Reasonably believing that there is one bullet and five empty chambers in the cylinder, Beth pulls the trigger.</text>
</example>

<example>
<paper_title>Can a risk of harm itself be a harm?</paper_title>
<type>thought_experiment</type>
<purpose>Challenges objective risk accounts by forcing precision about when exactly a risk constitutes harm and demonstrating the timing problem</purpose>
<context>Used to argue against Finkelstein's preference-based account of risk harm</context>
<text>Deadly Bingo: Beth has a sophisticated lottery ball machine that triggers a loaded gun the moment ball number 13 is drawn. The gun is pointing at Adam, who is sitting on a park bench blissfully unaware of Beth's contraption. Once the machine is turned on, twenty lottery balls spin in the container.</text>
</example>

<example>
<paper_title>Can a risk of harm itself be a harm?</paper_title>
<type>thought_experiment</type>
<purpose>Demonstrates that objective risks cannot interfere with interests by showing that perfect predictability renders the risk impotent without changing its objective probability</purpose>
<context>Used within the Deadly Bingo scenario to argue against objective risk accounts</context>
<text>Suppose that a perfect predictor, knowing all antecedent causes, could predict whether ball number 13 would be drawn when Beth turns on the machine. Since objective risks are mind-independent, the predictor's knowledge does not interfere with any causal processes. Suppose that the predictor perfectly predicts that ball number 13 will not be drawn. Does the objective risk nevertheless harm Adam? Since it is perfectly predicted that the risk is 'impotent', the risk's impact on Adam's interests is the same as pointing a certainly empty gun at Adam and pulling the trigger.</text>
</example>

<example>
<paper_title>Can a risk of harm itself be a harm?</paper_title>
<type>test_case</type>
<purpose>Illustrates the autonomy-based account of risk harm by showing how risks can allegedly make options unsafe</purpose>
<context>Presents Oberdiek's view that risks harm by limiting safe options</context>
<text>Beth laying a trap on a path makes Adam's option of using that path unsafe. Beth makes safe passage unavailable to Adam, and this in turn sets back his interest in having a range of acceptable alternatives from which to choose.</text>
</example>

<example>
<paper_title>Can a risk of harm itself be a harm?</paper_title>
<type>real_world_case</type>
<purpose>Provides the foundational scenario that motivates the entire philosophical investigation into whether risks themselves can be harms</purpose>
<context>Opens the paper and establishes the practical context for the theoretical debate</context>
<text>Beth drinks too much, gets into her car and attempts to drive home. With impaired reflexes and some swerves here and there, she continues her drive. On Beth's route is a pedestrian on the sidewalk, Adam, whom she narrowly misses. Adam is completely unaware of Beth's presence.</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>thought_experiment</type>
<purpose>Demonstrates the distinction between two kinds of failures in joint action - failing to do one's part versus acting disrespectfully</purpose>
<context>This is the central example used to establish the paper's main theoretical distinction</context>
<text>James and Paula are taking a walk together. James is ranting about the government but quickly realizes that Paula shows signs of discomfort. He immediately apologizes and continues the earlier, more successful, conversation about philosophy. But then James speeds up. This goes against Paula's intention to take a relaxing walk. 'Slow down, James! I don't want to walk so fast', she demands. John keeps walking and eventually, he is so far ahead of her that the ordinary concept of walking together no longer applies to them. Paula is confused. Did James not owe it to her to slow down? Did he not respect her enough to at least say goodbye?</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>test_case</type>
<purpose>Tests whether the distinction is merely one of degree rather than kind by flipping the scenario to show how mistakes can transform from innocent to disrespectful</purpose>
<context>Used to address the objection that the two failures are just different degrees of the same phenomenon</context>
<text>Imagine that James, instead of changing the topic, continues his rant, causing Paula to feel visibly uncomfortable. However, when he starts walking too fast and Paula tells him to slow down, he slows down immediately and even apologizes. But he keeps ranting. Has James's failure to act cooperatively by ranting suddenly become a case of disrespect as well as a failure to do his part relative to the joint intention to take an enjoyable, relaxing walk in the sun?</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>counterexample</type>
<purpose>Challenges the view that all failures in joint action constitute moral wrongdoing by showing innocent mistakes don't wrong one's partner</purpose>
<context>Used to argue against treating all joint action failures as instances of wronging</context>
<text>For example, if I build a flat-pack bed with my partner and, for some innocent reason, I use the wrong screw, I cause some frustration, but I do not wrong my partner. Such mistakes are bound to happen in any joint action. I do not need an excuse in such a case; I can admit that I made a mistake, say 'sorry' to signal that it was not due to a lack of cooperative intention, and we move on.</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>test_case</type>
<purpose>Shows that disrespect can occur even when joint intentions are fulfilled perfectly, demonstrating the independence of the two types of failure</purpose>
<context>Used to prove the distinction is one of kind rather than degree</context>
<text>The simplest example of the phenomenon of disrespect within a well-functioning joint action involves joint actions under coercion. If I force you to converse with me about the government, for example, because I have coercive power over you, I disrespect you because I disregard your rights and interests, say your right to act autonomously. You and I still share the intention to converse about the government but the only reason we share this intention is that I force you to.</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>real_world_case</type>
<purpose>Illustrates how the respect-based analysis explains experimental findings about notification versus permission in ending joint actions</purpose>
<context>Applied to make sense of empirical findings that challenge existing theories</context>
<text>Imagine I walk with you to work regularly, but we have never made any promises regarding this joint activity. We both change our minds and want the regular joint action to end. What I can do to end the practice is this: I notify you that I will not be coming anymore. I do not notify you because of some joint commitment or irreducible joint intention. I do it out of respect for your legitimate claims against me, which, again, are not grounded in the joint intention.</text>
</example>

<example>
<paper_title>Two kinds of failure in joint action: On disrespect and directed duties</paper_title>
<type>test_case</type>
<purpose>Tests the theory's ability to handle Gilbert's challenging case of coerced joint action by showing how the coercer loses claims to respectful treatment</purpose>
<context>Used to address a key objection to reductionist accounts of joint intention</context>
<text>For example, if a thief forces me to tell them the combination for the safe while threatening me with a gun, we can phrase this as a form of demand that is justified by the joint intention to help the criminal to open the safe, which we are coerced into against our desires and interests. However, the coercer has no grounds besides the joint intention on which they can make demands... By forcing me to engage in an immoral joint action, the criminal disrespects me in such a fundamental way that if the gun turns out to be fake, I have of course no obligations towards this person to notify or to seek permission to leave.</text>
</example>
</examples>

<analysis_example_patterns>
Key patterns for Analysis journal examples:
• **Concrete scenarios**: Real people in specific situations (Adam, Beth, Eve, James, Paula)
• **Clear philosophical work**: Each example tests theories, generates intuitions, or challenges views
• **Natural integration**: Examples flow within arguments rather than being set apart
• **Appropriate detail**: Enough specificity to be philosophically useful, not overwhelming
• **Variety of types**: Thought experiments, real cases, analogies, counterexamples, test cases
• **Direct presentation**: "Consider...", "Suppose...", clear setup without excessive hedging
• **Argumentative purpose**: Examples advance the argument, not just illustrate concepts
</analysis_example_patterns>
</philosophical_examples_from_analysis>"""

    def get_initial_development_prompt(
        self,
        move: str,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        move_index: int,
    ) -> str:
        """
        Construct prompt for initial development of a key move.

        This focuses on developing the core argument structure.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")

        # Get the outline sections that might be relevant
        outline_sections = outline.get("outline", "")

        # Get literature synthesis
        lit_synthesis = literature.get("synthesis", {})
        lit_narrative = literature.get("narrative", "")

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
- Phase I identified the paper topic and gathered literature
- Phase II.1 processed and analyzed the literature
- Phase II.2 created the paper framework (abstract, thesis, outline)
- We are now in Phase II.3, developing key argumentative moves
- After this, Phase II.4 will create a detailed outline integrating these key moves
- Phase III will focus only on prose crafting, not creating new arguments

Your task is to develop the intellectual content of this key move to completion.
</context>

<task>
Develop this philosophical key move in detail. Write the actual content as it would appear in the final paper.
Each key move is a critical argumentative step that advances the paper's thesis.
Make all intellectual decisions now - create complete arguments, not outlines or plans.
</task>

<input_data>
Key move to develop: "{move}"

Main thesis: "{main_thesis}"

Core contribution: "{core_contribution}"

This is move #{move_index + 1} in the paper's key argumentative structure.

Paper outline:
```
{outline_sections}
```
</input_data>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Each key move should be approximately 500-600 words maximum.
- Be selective and concise. Remove redundant examples or peripheral discussions.

# Content Requirements
Write the actual content for this key move AS IT WOULD APPEAR IN THE FINAL PAPER:
1. Write in scholarly philosophical prose, not meta-commentary
2. Develop a complete, well-structured philosophical argument
3. Include necessary background, premises, and conclusions
4. Connect this move to the paper's overall thesis
5. Make all intellectual decisions now
6. Be bold, interesting, and creative - this is for a top philosophy journal

# Strategic Decisions
Determine what this specific move needs:
- Concrete examples? (Use if conceptually complex or counter-intuitive)
- Literature engagement? (Cite only most directly relevant works)
- Development approach? (Conceptual analysis, case-based reasoning, etc.)

Choose the approach that best serves this specific argument.
</requirements>

<output_format>
Write in clear, crisp, engaging scholarly philosophical prose.

IMPORTANT:
- DO NOT write "Move Analysis", "Argument Structure", or similar headings
- DO NOT use bullet points or outline format
- DO NOT include phrases like "This move would..." or "This section will..."
- DO NOT merely parrot other philosophers' arguments - be ORIGINAL
- DO write in complete paragraphs as they would appear in the final paper
- DO develop all arguments fully with proper premises and conclusions
- DO write in scholarly style appropriate for publication
- DO be concise and focused - remember the 500-600 word target
</output_format>

<guidelines>
- Focus on philosophical depth and rigorous argument development
- Ensure logical coherence and theoretical soundness
- Keep the move realistic in scope while maintaining philosophical significance
- Consider both strengths and potential objections if applicable
- Prioritize philosophical precision and conciseness
- Remember: write the ACTUAL CONTENT, not commentary about it
</guidelines>"""

        return prompt

    def get_examples_development_prompt(
        self,
        move: str,
        current_development: Any,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for developing examples for a key move.

        This focuses on creating effective examples and illustrations to support the argument.
        """
        # Extract the current development content, handling various inputs
        if current_development is None:
            # If no current development provided, extract info from framework
            main_thesis = framework.get("main_thesis", "")
            moves_list = framework.get("key_moves", [])
            move_index = moves_list.index(move) if move in moves_list else -1

            current_content = f"""
# Key Move Context
This key move is: "{move}"

It supports the main thesis: "{main_thesis}"

Please develop examples that illustrate and support this move.
"""
        elif isinstance(current_development, dict):
            current_content = current_development.get("content", "")
        else:
            current_content = str(current_development)

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are developing examples for a key move that has already been drafted.
Your examples must be fully developed and written as they would appear in the published paper.
Later phases will focus only on prose refinement, not creating new examples.
</context>

{self.curated_examples_database}

<task>
Develop examples for this key move AS THEY WOULD APPEAR IN THE FINAL PAPER.
Write fully developed examples in scholarly philosophical prose.
Only include examples if they genuinely clarify or strengthen the argument.
Study the Analysis examples above to understand what makes examples do real philosophical work.
</task>

<current_development>
{current_content}
</current_development>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Be extremely selective with examples.
- Each example should be concise yet effective - quality over quantity.
- Only include examples if they genuinely clarify or strengthen the argument.

# Content Requirements
1. Write fully developed examples in scholarly philosophical prose
2. Present examples as they would appear in the published paper
3. Integrate examples naturally within the philosophical argument
4. Include complete details and necessary context
5. Make all intellectual decisions now

# Strategic Considerations
Determine whether this move truly needs examples:
- If already clear without examples, state no additional examples needed
- If examples would strengthen, develop only the most essential ones
- Focus on quality over quantity - one perfect example beats several mediocre ones

# Analysis Example Patterns to Follow
Based on the curated examples above, note how Analysis uses:
- **Concrete characters**: Real people in specific situations (Adam, Beth, Eve)
- **Clear philosophical purpose**: Each example tests theories or generates intuitions
- **Natural presentation**: "Consider...", "Suppose..." without excessive setup
- **Appropriate scope**: Detailed enough to be useful, not overwhelming
- **Argumentative integration**: Examples advance arguments, not just illustrate
</requirements>

<output_format>
Write examples in clear, concise scholarly philosophical prose.

IMPORTANT:
- DO NOT use phrases like "This example would..." or "This case could..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or "future development" references
- DO write examples as complete, detailed, and publication-ready
- DO integrate examples naturally into the philosophical argument
- DO include all necessary context and details
- DO be concise - every word must earn its place
- DO follow Analysis patterns from the curated examples above
</output_format>

<guidelines>
- Choose philosophically illuminating examples, not just illustrative ones
- Ensure examples are clear while maintaining philosophical rigor
- Examples should genuinely strengthen the argument, not repeat it
- Consider both supporting examples and potential counterexamples
- Focus on quality over quantity
- Remember: write ACTUAL EXAMPLES as they would appear in the paper
- Study the Analysis patterns above for concrete guidance on example construction
</guidelines>"""

        return prompt

    def get_literature_integration_prompt(
        self,
        move: str,
        current_development: Any,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for integrating literature into a key move.

        This focuses on connecting the move to relevant philosophical literature.
        """
        # Extract the current development content, handling various inputs
        if current_development is None:
            # If no current development provided, extract info from framework
            main_thesis = framework.get("main_thesis", "")
            moves_list = framework.get("key_moves", [])
            move_index = moves_list.index(move) if move in moves_list else -1

            current_content = f"""
# Key Move Context
This key move is: "{move}"

It supports the main thesis: "{main_thesis}"

Please integrate relevant literature with this move.
"""
        elif isinstance(current_development, dict):
            current_content = current_development.get("content", "")
        else:
            current_content = str(current_development)

        # Extract literature information
        lit_readings = literature.get("readings", {})
        lit_synthesis = literature.get("synthesis", {})
        lit_narrative = literature.get("narrative", "")

        # Extract some key literature info to include in the prompt
        lit_summary = ""
        if lit_synthesis:
            themes = lit_synthesis.get("themes", [])
            lit_summary = "Key themes in the literature:\n"
            for theme in themes[
                :3
            ]:  # Limit to first 3 themes to keep prompt size reasonable
                theme_name = theme.get("name", "")
                theme_desc = theme.get("description", "")
                lit_summary += f"- {theme_name}: {theme_desc}\n"

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are integrating relevant literature into a key move that has been developed.
The literature integration must be written as it would appear in the published paper.
Later phases will focus only on prose refinement, not creating new literature connections.
</context>

<task>
Integrate relevant literature into this key move AS IT WOULD APPEAR IN THE FINAL PAPER.
Write scholarly philosophical prose that naturally incorporates literature.
Position the move properly within the philosophical landscape.
Be highly selective - only cite what's truly necessary.
</task>

<current_development>
{current_content}
</current_development>

<literature_context>
{lit_summary}
</literature_context>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Be extremely selective with citations.
- Cite only the most directly relevant works providing essential context.
- Avoid literature "surveys" listing multiple authors making similar points.
- Focus on how your argument extends beyond, challenges, or synthesizes existing views.

# Content Requirements
1. Write scholarly philosophical prose that naturally incorporates literature
2. Present literature engagement as it would appear in the published paper
3. Cite and discuss relevant works substantively, not superficially
4. Position the move properly within the philosophical landscape
5. Make all intellectual decisions now

# Strategic Considerations
Determine whether and how this move needs literature engagement:
- Novel argument? Focus on positioning within existing debates
- Responding to specific views? Engage directly with primary sources
- Extending existing work? Clarify your original contribution
- In all cases, be highly selective - only cite what's necessary
</requirements>

<output_format>
Write literature integration in clear scholarly philosophical prose.

IMPORTANT:
- DO NOT use phrases like "This would connect to..." or "The author could cite..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or "future development" references
- DO write with proper scholarly citations as they would appear
- DO engage with philosophical content of cited works, not just name-drop
- DO position the move within relevant philosophical debates
- DO be selective and focused - every citation should advance the argument
</output_format>

<guidelines>
- Focus on quality of engagement rather than quantity of citations
- Literature should genuinely strengthen the argument
- Engage with both supporting and challenging perspectives when necessary
- Demonstrate how the move advances beyond existing work
- Remember: write ACTUAL LITERATURE INTEGRATION as it would appear
</guidelines>"""

        return prompt

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
