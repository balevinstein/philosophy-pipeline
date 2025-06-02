# Phase II.2 Mechanical Improvements Plan

## Prompt Classes to Update

### Abstract Workflow (3/9 classes) ✅
- [x] AbstractDevelopmentPrompts - DONE
- [x] AbstractCriticPrompts - DONE  
- [x] AbstractRefinementPrompts - DONE

### Outline Workflow (3/9 classes) ✅
- [x] OutlineDevelopmentPrompts - DONE
- [x] OutlineCriticPrompts - DONE
- [x] OutlineRefinementPrompts - DONE

### Key Moves Workflow (3/9 classes) ✅
- [x] KeyMovesDevelopmentPrompts - DONE
- [x] KeyMovesCriticPrompts - DONE
- [x] KeyMovesRefinementPrompts - DONE

## Mechanical Improvements Applied ✅

1. **Add system_prompt attribute** ✅
   - Development: "You are an expert philosophy researcher..."
   - Critic: "You are a rigorous philosophy journal reviewer..."
   - Refinement: "You are an expert philosophy editor..."

2. **Add XML structure tags** ✅
   - `<context>` - Pipeline awareness
   - `<task>` - Clear task description
   - `<requirements>` - Specific requirements
   - `<output_format>` - Expected output structure
   - `<thinking>` - For reasoning (where appropriate)

3. **Add JSON formatting rules** (for JSON outputs) ✅
   ```
   CRITICAL JSON FORMATTING RULES:
   1. Output ONLY valid JSON - no markdown code blocks
   2. Use double quotes for all strings
   3. Escape quotes within text using \"
   4. Replace newlines with spaces in text fields
   5. Ensure all brackets and braces are properly closed
   ```

4. **Add pipeline context** ✅
   - Which phase this is
   - What comes before/after
   - That output will be parsed by code

5. **Add method: get_system_prompt()** ✅
   - Returns the system prompt for API calls

## Order of Implementation

1. First complete Abstract workflow ✅
2. Then Outline workflow ✅
3. Finally Key Moves workflow ✅

## Notes

- Keep changes mechanical/structural only for now ✅
- Advanced prompt patterns (skeptical friend, etc.) will be added in a second pass
- Ensure API handler can use system prompts from these classes

## Summary

All 9 prompt classes in Phase II.2 have been successfully updated with mechanical improvements. The prompts now have:
- Clear system prompts defining roles
- XML structure for better organization
- Pipeline awareness and context
- JSON formatting rules where applicable
- Consistent get_system_prompt() methods

Ready for testing or advanced prompt pattern integration! 