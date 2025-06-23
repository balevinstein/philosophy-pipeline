#!/usr/bin/env python3
"""
Philosophical Example Extraction Pipeline
Extracts examples and other key philosophical moves from Analysis papers
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

from src.utils.api import APIHandler, load_config


class PhilosophicalExampleExtractor:
    """Extracts philosophical examples from Analysis papers"""
    
    def __init__(self):
        self.config = load_config()
        self.api_handler = APIHandler(self.config)
        self.output_dir = Path("./extracted_examples")
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_paper_title(self, pdf_path: Path) -> str:
        """Extract the actual paper title from PDF content"""
        try:
            print(f"Extracting paper title from {pdf_path.name}...")
            
            title_extraction_prompt = """
Please extract the title of this philosophy paper from the PDF.
Return only the paper title, nothing else.
The title is usually prominently displayed at the top of the first page.
Do not include author names, journal information, or other metadata.
"""
            
            response = self.api_handler.make_api_call(
                stage="move_development",
                prompt=title_extraction_prompt,
                pdf_paths=[pdf_path],
                system_prompt=None
            )
            
            # Clean up the response to get just the title
            title = response.strip().strip('"').strip("'")
            print(f"Extracted title: {title}")
            return title
            
        except Exception as e:
            print(f"Error extracting title from {pdf_path}: {str(e)}")
            # Fallback to filename
            return pdf_path.stem
    
    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract clean text from PDF using existing API infrastructure"""
        try:
            # Use the same PDF processing as the main pipeline
            # This leverages existing API infrastructure for consistency
            print(f"Extracting text from {pdf_path.name}...")
            
            # For now, we'll use the API with the PDF directly and a simple prompt
            # to get clean text representation
            text_extraction_prompt = """
Please provide a clean, readable text version of this PDF document.
Remove headers, footers, page numbers, and formatting artifacts.
Preserve paragraph structure and maintain the logical flow of the text.
Focus on the main philosophical content.
"""
            
            response = self.api_handler.make_api_call(
                stage="move_development",  # Use existing stage config
                prompt=text_extraction_prompt,
                pdf_paths=[pdf_path],
                system_prompt=None
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def extract_examples_from_text(self, text: str, paper_title: str) -> List[Dict[str, Any]]:
        """Use Claude to identify and extract philosophical examples from text"""
        
        extraction_prompt = f"""
You are analyzing a philosophy paper from the journal Analysis to extract examples that do real philosophical work.

<paper_title>{paper_title}</paper_title>

<task>
Identify concrete examples, cases, thought experiments, or scenarios that serve specific philosophical purposes - NOT mere illustrations. Look for:

- Examples that demonstrate concepts
- Cases that test theories  
- Thought experiments that generate intuitions
- Real-world scenarios that show distinctions
- Counterexamples that challenge views
- Analogies that illuminate arguments

DO NOT include:
- Mere references to other philosophers' examples
- Abstract theoretical statements
- Literature reviews or citations
- General claims without concrete scenarios
</task>

<output_format>
For each example found, provide:

```xml
<example>
<type>[thought_experiment|real_world_case|analogy|counterexample|test_case]</type>
<purpose>[what specific philosophical work this example does]</purpose>
<context>[brief context of where this appears in the argument]</context>
<text>[the actual example text, preserving the author's language]</text>
</example>
```

Only extract examples that genuinely advance philosophical arguments.
Preserve the author's original language and phrasing.
Be selective - quality over quantity.
</output_format>

<paper_text>
{text}
</paper_text>
"""

        try:
            print(f"Extracting examples from {paper_title}...")
            
            response = self.api_handler.make_api_call(
                stage="move_development",  # Use existing stage config
                prompt=extraction_prompt,
                system_prompt=None
            )
            
            # Parse the examples from the response
            examples = self._parse_examples_from_response(response, paper_title)
            return examples
            
        except Exception as e:
            print(f"Error extracting examples: {str(e)}")
            return []
    
    def _parse_examples_from_response(self, response: str, paper_title: str) -> List[Dict[str, Any]]:
        """Parse examples from Claude's XML response"""
        examples = []
        
        try:
            # Look for XML blocks in the response
            lines = response.split('\n')
            current_example = {}
            in_example = False
            current_field = None
            content_lines = []
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('<example>'):
                    in_example = True
                    current_example = {'paper_title': paper_title}
                    current_field = None
                    content_lines = []
                elif line.startswith('</example>'):
                    if current_field and content_lines:
                        current_example[current_field] = '\n'.join(content_lines).strip()
                    if current_example and 'text' in current_example:
                        examples.append(current_example.copy())
                    in_example = False
                    current_example = {}
                elif in_example:
                    if line.startswith('<type>'):
                        current_field = 'type'
                        content = line.replace('<type>', '').replace('</type>', '')
                        if content:
                            current_example['type'] = content
                    elif line.startswith('<purpose>'):
                        current_field = 'purpose'  
                        content = line.replace('<purpose>', '').replace('</purpose>', '')
                        if content:
                            current_example['purpose'] = content
                        else:
                            content_lines = []
                    elif line.startswith('<context>'):
                        current_field = 'context'
                        content = line.replace('<context>', '').replace('</context>', '')
                        if content:
                            current_example['context'] = content
                        else:
                            content_lines = []
                    elif line.startswith('<text>'):
                        current_field = 'text'
                        content = line.replace('<text>', '').replace('</text>', '')
                        if content:
                            current_example['text'] = content
                        else:
                            content_lines = []
                    elif line.startswith('</'):
                        if current_field and content_lines:
                            current_example[current_field] = '\n'.join(content_lines).strip()
                        current_field = None
                        content_lines = []
                    elif current_field:
                        content_lines.append(line)
            
            print(f"Extracted {len(examples)} examples from {paper_title}")
            return examples
            
        except Exception as e:
            print(f"Error parsing examples: {str(e)}")
            return []
    
    def create_examples_database(self, examples_list: List[Dict[str, Any]]) -> str:
        """Create XML database of all extracted examples"""
        
        root = ET.Element("philosophical_examples")
        
        for example in examples_list:
            example_elem = ET.SubElement(root, "example")
            
            # Add paper title
            title_elem = ET.SubElement(example_elem, "paper_title")
            title_elem.text = example.get('paper_title', '')
            
            # Add type
            type_elem = ET.SubElement(example_elem, "type")
            type_elem.text = example.get('type', '')
            
            # Add purpose
            purpose_elem = ET.SubElement(example_elem, "purpose")
            purpose_elem.text = example.get('purpose', '')
            
            # Add context
            context_elem = ET.SubElement(example_elem, "context")
            context_elem.text = example.get('context', '')
            
            # Add text
            text_elem = ET.SubElement(example_elem, "text")
            text_elem.text = example.get('text', '')
        
        # Pretty print the XML
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def process_papers(self, paper_paths: List[Path]) -> str:
        """Process multiple papers and create combined examples database"""
        all_examples = []
        
        for paper_path in paper_paths:
            print(f"\nProcessing {paper_path.name}...")
            
            # Extract actual paper title
            paper_title = self.extract_paper_title(paper_path)
            
            # Extract text
            text = self.extract_pdf_text(paper_path)
            if not text:
                print(f"Failed to extract text from {paper_path.name}")
                continue
            
            # Extract examples
            examples = self.extract_examples_from_text(text, paper_title)
            all_examples.extend(examples)
            
            # Save individual results using filename for the file
            individual_file = self.output_dir / f"{paper_path.stem}_examples.json"
            with open(individual_file, 'w') as f:
                json.dump(examples, f, indent=2)
            
            print(f"Saved {len(examples)} examples to {individual_file}")
            
            # Rate limiting
            time.sleep(2)
        
        # Create combined XML database
        if all_examples:
            xml_database = self.create_examples_database(all_examples)
            
            # Save XML database
            xml_file = self.output_dir / "philosophical_examples_database.xml"
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_database)
            
            # Save JSON backup
            json_file = self.output_dir / "philosophical_examples_database.json"
            with open(json_file, 'w') as f:
                json.dump(all_examples, f, indent=2)
            
            print(f"\n✅ Created examples database with {len(all_examples)} examples")
            print(f"📄 XML: {xml_file}")
            print(f"📄 JSON: {json_file}")
            
            return xml_database
        
        return ""


def main():
    """Extract examples from specified Analysis papers"""
    extractor = PhilosophicalExampleExtractor()
    
    # Target papers identified by user
    paper_paths = [
        Path("Analysis_papers/anab031.pdf"),
        Path("Analysis_papers/anab033.pdf"),
        Path("Analysis_papers/anae045 (1).pdf")
    ]
    
    # Verify papers exist
    available_papers = [p for p in paper_paths if p.exists()]
    if not available_papers:
        print("❌ No target papers found!")
        return
    
    print(f"🎯 Processing {len(available_papers)} Analysis papers for examples...")
    print(f"Papers: {[p.name for p in available_papers]}")
    
    # Extract examples
    database = extractor.process_papers(available_papers)
    
    if database:
        print("🎉 Example extraction completed successfully!")
        print("\nNext steps:")
        print("1. Review extracted_examples/ directory")  
        print("2. Integrate XML into Phase II.3 prompts")
        print("3. Test with enhanced examples guidance")
    else:
        print("❌ No examples extracted")


if __name__ == "__main__":
    main() 