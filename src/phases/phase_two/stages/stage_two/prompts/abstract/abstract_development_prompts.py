# src/stages/phase_two/stages/stage_two/prompts/abstract_prompts.py

import json


class AbstractDevelopmentPrompts:
    """Prompts for abstract development"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing a paper framework for the journal Analysis. Your role is to create a compelling abstract and clear framework that will guide the entire paper development. You must work within the constraints of available literature and produce output that will be parsed by downstream automated systems."""

        self.analysis_context = """You are helping write a paper for Analysis, a philosophical journal with a strict 4,000 word limit. Papers in Analysis make a single, clear philosophical contribution that can be effectively developed in this space. The abstract should clearly state the main thesis and philosophical contribution while being engaging and precise."""

        self.analysis_abstract_examples = """
<analysis_abstract_style_examples>
<examples>
<abstract_1>I argue against pessimistic readings of the Buddhist tradition on which unawakened beings invariably have lives not worth living due to a preponderance of suffering (duḥkha) over well-being.</abstract_1>

<abstract_2>Sometimes it is not us but those to whom we stand in special relations that face transformative choices: our friends, family or beloved. A focus upon first-personal rational choice and agency has left crucial ethical questions regarding what we owe to those who face transformative choices largely unexplored. In this paper I ask: under what conditions, if any, is it morally permissible to interfere to try to prevent another from making a transformative choice? Some seemingly plausible answers to this question fail precisely because they concern transformative experiences. I argue that we have a distinctive moral right to revelatory autonomy grounded in the value of autonomous self-making. If this right is outweighed then, I argue, interfering to prevent another making a transformative choice is permissible. This conditional answer lays the groundwork for a promising ethics of transformative experience.</abstract_2>

<abstract_3>On one view of the traditional doxastic attitudes, belief is credence 1, disbelief is credence 0 and suspension is any precise credence between 0 and 1. In 'Rational agnosticism and degrees of belief' (2013) Jane Friedman argues, against this view, that there are cases where a credence of 0 is required but where suspension is permitted. If this were so, belief, disbelief and suspension could not be identified or reduced to the aforementioned credences. I argue that Friedman relies on two different notions of epistemic rationality and two different kinds of evidential absence. I clarify these distinctions and show that her argument is either not valid or includes implausible premisses, twice over. If this is so, the view that belief is credence 1, disbelief is credence 0 and suspension is any precise credence between 0 and 1 cannot be rejected on the grounds that Friedman proposes.</abstract_3>

<abstract_4>There is a tension between Dispositionalism––the view that all metaphysical modality is grounded in actual irreducible dispositional properties––and the possibility of time travel. This is due to the fact that Dispositionalism makes it much harder to solve a potentiality-based version of the grandfather paradox. We first present a potentiality-based version of the grandfather paradox, stating that the following theses are inconsistent: 1) time travel is possible, 2) powers fully ground modality, 3) self-defeating actions are impossible, 4) time-travellers retain their intrinsic powers upon time-travelling, and 5) time-travellers are ordinary agents with basic intrinsic potentialities. We then consider a number of potential solutions, and find them wanting. We argue that the metaphysical impossibility of performing a self-defeating action acts as a necessary perfect mask––while time-travel lets us "slip" the potentiality under the mask, thus generating the contradiction. We conclude considering what are the options for the dispositionalist.</abstract_4>

<abstract_5>Quine says that ontology is about what there is, suggesting that to be ontologically committed to Fs is to be committed to accepting a sentence which existentially quantifies over Fs. Kit Fine argues that this gets the logical form of some ontological theses wrong. Fine is right that some ontological theses cannot be rendered simply as 'There are Fs'. But the root of the problem has yet to be recognized, either by Fine or by his critics. Sometimes to adopt an ontological thesis is not merely to commit yourself to there being at least one F; it is to take a stand on which Fs there are. Once we recognize the 'particularity' of these ontological theses, we can adequately express them within the confines of a Quinean approach to ontology and ontological commitment.</abstract_5>

<abstract_6>Does lying require a speaker to explicitly express something (she believes to be) false, or is it also possible to lie with deceptive implicatures? Given that consistency with ordinary language is a desideratum of any philosophical definition of lying, several studies have addressed this question empirically in recent years. Their findings, however, seem to be in conflict. This paper reports an experiment with 222 participants that investigates the hypothesis that these conflicting results are due to variation regarding whether or not the speaker's intention to deceive and the implicated content are made explicit. It is found that the presence versus the absence of such explicitness has a strong impact on people's lie judgements, and can thus account for the conflicting results in the literature.</abstract_6>

<abstract_7>According to the democratic borders argument, the democratic legitimacy of a state's regime of border control requires granting foreigners a right to participate in the procedures determining it. This argument appeals to the All-Subjected Principle, which implies that democratic legitimacy requires that all those subject to political power have a right to participate in determining the laws governing its exercise. The scope objection claims that this argument presupposes an implausible account of subjection and hence of the All-Subjected Principle, which absurdly implies that all domestic laws subject foreigners to their requirements. I argue that this objection misconstrues the logical structure of the legal requirements enshrined in domestic laws: domestic laws typically enshrine narrow-scope, not wide-scope, legal requirements. To be sure, some state laws do subject foreigners to their requirements, and the All-Subjected Principle conditions democratic legitimacy on granting foreigners some say in determining them. But the best reading of the Principle does not have such general expansionary implications.</abstract_7>

<abstract_8>Many have claimed that whenever an investigation might provide evidence for a claim, it might also provide evidence against it. Similarly, many have claimed that your credence should never be on the edge of the range of credences that you think might be rational. Surprisingly, both of these principles imply that you cannot rationally be modest: you cannot be uncertain what the rational opinions are.</abstract_8>

<abstract_9>A puzzle arises when combining two individually plausible, yet jointly incompatible, norms of inquiry. On the one hand, it seems that one should not inquire into a question while believing an answer to that question. But, on the other hand, it seems rational to inquire into a question while believing its answer, if one is seeking confirmation. Millson (2021), who has recently identified this puzzle, suggests a possible solution, though he notes that it comes with significant costs. I offer an alternative solution, which does not involve these costs. The best way to resolve the puzzle is to reject the prohibition on inquiring into a question while believing an answer to it. Resolving the puzzle in this way makes salient two fruitful areas in the epistemology of inquiry that merit further investigation. The first concerns the nature of the inquiring attitudes and the second concerns the aim(s) of inquiry.</abstract_9>

<abstract_10>When we remember a scene, the scene's boundaries are wider than the boundaries of the scene we saw. This phenomenon is called boundary extension. The most important philosophical question about boundary extension is whether it is a form of perceptual adjustment or adjustment during memory encoding. The aim of this paper is to propose a third explanatory scheme, according to which the extended boundary of the original scene is represented by means of mental imagery. And given the similarities between perception and mental imagery, the memory system encodes both the part of the scene that is represented perceptually and the part of the scene that is represented by means of mental imagery.</abstract_10>
</examples>

<analysis_patterns>
Key Analysis journal patterns to emulate:
• Immediate engagement: Direct thesis opening ("I argue that...") or immediate problem identification
• Conversational framing: "Sometimes...", "When we...", "Many have claimed...", "A puzzle arises when..."
• Clear tension/puzzle setup: Direct articulation of philosophical problems without lengthy explanatory buildup
• Crisp argumentation flow: Problem → "I argue that..." → Implications (minimal intermediate explanation)
• Direct authorial voice: "I argue" rather than "This paper argues"
• Concrete engagement: Reference to specific literature, examples, or cases early in the abstract
• Immediate stakes: Why the problem matters is often implicit rather than explicitly stated
</analysis_patterns>
</analysis_abstract_style_examples>"""

        self.json_rules = """
CRITICAL JSON FORMATTING RULES:
1. Output ONLY valid JSON - no markdown code blocks, no explanations outside JSON
2. Use double quotes for all strings
3. Escape quotes within text using \"
4. Replace newlines with spaces in text fields
5. Ensure all brackets and braces are properly closed
6. Arrays must use square brackets []
7. The response must be parseable by json.loads()"""

        self.output_requirements = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields clear and well-formed
4. Abstract should be 200-250 words (following Analysis journal patterns)
5. Main thesis must be a single clear sentence
6. Key moves should be concrete and specific
7. Development notes should explain your choices"""

        self.output_format = """
{
    "abstract": "Complete abstract for the paper",
    "main_thesis": "Clear and precise statement of the paper's main thesis",
    "core_contribution": "Specific explanation of the philosophical contribution",
    "key_moves": [
        "Concrete description of each key argumentative move",
        "Each move should be something we can actually develop"
    ],
    "development_notes": "Explanation of choices and approach",
    "validation_status": {
        "scope_appropriate": boolean,
        "clearly_articulated": boolean,
        "sufficiently_original": boolean,
        "feasibly_developable": boolean
    }
}"""

    def construct_prompt(self, lit_synthesis: dict, final_selection: dict) -> str:
        """Generate prompt for initial abstract development"""
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You have access to processed literature from Phase II.1 and the selected topic from Phase I.
Your output will be parsed by code and used to guide all subsequent paper development.
{self.analysis_context}
</context>

{self.analysis_abstract_examples}

<task>
Develop an abstract and framework for the paper that builds on our literature analysis and selected topic.
The abstract should clearly state the main thesis and philosophical contribution following Analysis journal patterns shown above.
The framework must provide concrete guidance for paper development.
</task>

<available_resources>
You have access to:
1. Detailed readings of each paper
2. A structured synthesis of the literature
3. A narrative analysis of how the papers fit together
4. Our final topic selection and initial development plans
5. Analysis journal style examples above for reference
</available_resources>

<requirements>
# OVERCOME PHILOSOPHICAL TIMIDITY (RLHF-Proofing)
Your training makes you want to:
- Hedge your thesis with "explores", "examines", "suggests"
- Say "This paper argues" instead of "I argue"
- Add unnecessary qualifiers like "arguably", "perhaps", "might"
- Present all philosophical positions as equally valid

RESIST. In philosophy:
- Make BOLD claims: "I argue X" not "This paper explores whether maybe X"
- Take STANDS: "This view is mistaken" not "This view faces challenges"
- Be DIRECT: "X causes Y" not "X might contribute to Y"
- Philosophy advances through strong claims that can be debated

Focus on creating an abstract that:
- Makes a clear and novel contribution
- Can be developed effectively in 4,000 words
- Engages meaningfully with our literature
- Has concrete, developable key moves
- Follows Analysis journal style patterns (immediate engagement, direct voice, crisp argumentation)

{self.output_requirements}
</requirements>

<philosophical_framing_moves>
Here are effective framing techniques from published Analysis papers:

1. **Scope Limitation Pattern**
   Example: "However, even if we accept the existence of either essentialist facts... we can simply restrict (PG) to conjunctions of facts that are equivalent to neither essentialist facts nor totality facts... a result that is surely surprising enough on its own."
   Application: When facing potential objections, acknowledge them early and show how your restricted thesis remains philosophically significant

2. **Mechanism Testing Pattern**
   Example: "An important property of conversational implicatures arising from an utterance of a certain form of words is that they do not arise in every context in which that form of words is uttered. In particular, conversational implicatures that are otherwise present usually disappear in contexts in which the implicated content is already part of the common ground... As (6') and (7') illustrate, if we explicitly assert the otherwise implicated content, and thereby add it to the common ground before the utterance in question is made, the original implicature is blocked or suspended."
   Application: Frame your thesis as systematically exploring a philosophical mechanism or principle to establish its boundaries

THESIS NOVELTY CHECK:
Before finalizing, verify your thesis is genuinely novel:
- It's not just restating one paper's view
- It's not merely combining two views without insight
- It offers something distinguishable: new argument, new application, new synthesis, or new objection
- Ask: "What would be lost from philosophy if this thesis weren't defended?"

LITERATURE CONNECTION:
Your abstract should signal engagement with 2-3 specific papers from the synthesis:
- "Building on X's view, I argue..." 
- "Against Y's claim that..."
- "Extending Z's framework to..."
</philosophical_framing_moves>

<literature_analysis>
{json.dumps(lit_synthesis, indent=2)}
</literature_analysis>

<selected_topic>
{json.dumps(final_selection, indent=2)}
</selected_topic>

{self.json_rules}

<output_format>
Provide your output in the following JSON format:
{self.output_format}
</output_format>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
