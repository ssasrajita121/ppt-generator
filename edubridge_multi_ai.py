import streamlit as st
import subprocess
import tempfile
import os
import json
import re
from datetime import datetime

# Page config
st.set_page_config(
    page_title="EduBridge AI PPT Generator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2D3748;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4299E1;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        font-weight: bold;
    }
    .success-box {
        background-color: #C6F6D5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #38A169;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #BEE3F8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4299E1;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'template_configured' not in st.session_state:
    st.session_state.template_configured = False
if 'brand_config' not in st.session_state:
    st.session_state.brand_config = {
        'company_name': 'EduBridge',
        'tagline_1': "India's leading Workforce Development Platform that helps learners in building careers",
        'tagline_2': "with leading corporates through training & other career building services.",
        'hashtag': '#letslearntoearn',
        'footer_text': 'All rights reserved.',
        'colors': {
            'yellow': 'F9D54A',
            'green': '4EDA3B',
            'teal': '2DD4BF',
            'blue': '5B9FD8',
            'coral': 'F96167',
            'purple': '9D4EDD',
            'cream': 'F5E6D3',
            'darkText': '2D3748',
            'lightText': '718096',
            'white': 'FFFFFF'
        },
        'font': 'Calibri'
    }

# Header
st.markdown('<div class="main-header">🎓 EduBridge AI PPT Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-AI Support: Claude & Gemini</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/F9D54A/2D3748?text=EduBridge", width=200)
    
    st.markdown("### 🤖 AI Provider Selection")
    
    ai_provider = st.radio(
        "Choose AI Provider",
        ["Anthropic Claude", "Google Gemini"],
        help="Select which AI to use for content generation"
    )
    
    st.markdown("---")
    st.markdown("### 🔑 API Settings")
    
    if ai_provider == "Anthropic Claude":
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Get from: console.anthropic.com"
        )
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        
        st.info("**Model:** Claude Sonnet 4.5")
        
    else:  # Google Gemini
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Get from: aistudio.google.com/apikey"
        )
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY", "")
        
        st.info("**Model:** Gemini 1.5 Pro")
    
    st.markdown("---")
    
    # Template Configuration
    st.markdown("### 🎨 Template Configuration")
    
    if st.button("⚙️ Configure Brand Template"):
        st.session_state.show_config = True
    
    if st.session_state.template_configured:
        st.success("✅ Template Configured")
    else:
        st.info("💡 Using default EduBridge template")
    
    st.markdown("---")
    
    st.markdown("### 🧠 How It Works")
    st.markdown(f"""
    **AI Provider:** {ai_provider} 🤖
    
    **Layer 1: Your Branding** 🎨
    - Fixed header & footer
    - Company colors & fonts
    
    **Layer 2: AI Layouts** 🤖
    - Analyzes content type
    - Picks best visual layout
    - Smart & adaptive
    """)

# Configuration Modal
if st.session_state.get('show_config', False):
    st.markdown("---")
    st.markdown("## ⚙️ Brand Template Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Company Information")
        company_name = st.text_input("Company Name", value=st.session_state.brand_config['company_name'])
        tagline_1 = st.text_area("Tagline Line 1", value=st.session_state.brand_config['tagline_1'], height=60)
        tagline_2 = st.text_area("Tagline Line 2", value=st.session_state.brand_config['tagline_2'], height=60)
        hashtag = st.text_input("Hashtag", value=st.session_state.brand_config['hashtag'])
        footer_text = st.text_input("Footer Text", value=st.session_state.brand_config['footer_text'])
    
    with col2:
        st.markdown("#### Brand Colors (Hex without #)")
        colors = st.session_state.brand_config['colors']
        
        col_a, col_b = st.columns(2)
        with col_a:
            yellow = st.text_input("Color 1", value=colors['yellow'])
            green = st.text_input("Color 2", value=colors['green'])
            teal = st.text_input("Color 3", value=colors['teal'])
            blue = st.text_input("Color 4", value=colors['blue'])
        with col_b:
            coral = st.text_input("Color 5", value=colors['coral'])
            purple = st.text_input("Color 6", value=colors['purple'])
            cream = st.text_input("Background", value=colors['cream'])
            darkText = st.text_input("Text Color", value=colors['darkText'])
    
    col_save, col_cancel = st.columns([1, 1])
    
    with col_save:
        if st.button("💾 Save Template", use_container_width=True):
            st.session_state.brand_config = {
                'company_name': company_name,
                'tagline_1': tagline_1,
                'tagline_2': tagline_2,
                'hashtag': hashtag,
                'footer_text': footer_text,
                'colors': {
                    'yellow': yellow, 'green': green, 'teal': teal, 'blue': blue,
                    'coral': coral, 'purple': purple, 'cream': cream, 'darkText': darkText,
                    'lightText': colors['lightText'], 'white': colors['white']
                },
                'font': 'Calibri'
            }
            st.session_state.template_configured = True
            st.session_state.show_config = False
            st.success("✅ Template saved!")
            st.rerun()
    
    with col_cancel:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_config = False
            st.rerun()
    
    st.markdown("---")

# Main content
if not st.session_state.get('show_config', False):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Presentation Details")
        
        topic = st.text_input(
            "Presentation Topic *",
            placeholder="e.g., Customer Service Excellence, Introduction to Python",
        )
        
        slide_count = st.slider(
            "Number of Content Slides (excluding title slide)",
            min_value=3,
            max_value=10,
            value=5
        )
        
        instructions = st.text_area(
            "Additional Instructions (Optional)",
            placeholder="e.g., Focus on practical examples, Include case studies",
            height=100
        )
    
    with col2:
        st.markdown("### 📊 Preview")
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **Your Presentation:**
        - 🎯 Total slides: **{slide_count + 1}**
        - 🤖 AI Provider: **{ai_provider}**
        - 🎨 Branding: **{st.session_state.brand_config['company_name']}**
        - 📐 Format: **16:9 Widescreen**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🎨 AI Layout Options")
        st.info("""
        - 📋 Definition Boxes
        - 📊 Split Layouts
        - 🎯 Icon Grids
        - 🔢 Numbered Boxes
        - ⚖️ Comparison Tables
        - 🔄 Flow Diagrams
        - 📦 Three Boxes
        """)
    
    st.markdown("---")
    
    if st.button("🚀 Generate Presentation", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {ai_provider} API key in the sidebar")
        elif not topic:
            st.error("⚠️ Please enter a presentation topic")
        else:
            try:
                with st.spinner("🎨 Creating your presentation..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: AI analyzes content
                    status_text.text(f"🧠 {ai_provider} analyzing content...")
                    progress_bar.progress(15)
                    
                    analysis_prompt = f"""You are a presentation design expert. Create a slide structure for: "{topic}"

Create {slide_count + 1} slides (1 title + {slide_count} content).

{f'Requirements: {instructions}' if instructions else ''}

For EACH slide:
1. Determine content type
2. Select BEST layout from: definition_boxes, split_layout, icon_grid, numbered_boxes, comparison_table, flow_diagram, three_boxes
3. Provide appropriate content

Return ONLY valid JSON:
{{
  "slides": [
    {{
      "slideNumber": 1,
      "title": "Main Title",
      "subtitle": "Optional tagline",
      "isTitle": true
    }},
    {{
      "slideNumber": 2,
      "title": "Slide Title",
      "layout": "definition_boxes",
      "reasoning": "Why this layout",
      "content": {{
        "definition": "Explanation text",
        "boxes": ["Point 1", "Point 2", "Point 3"]
      }}
    }}
  ]
}}"""

                    # Call appropriate AI
                    if ai_provider == "Anthropic Claude":
                        slide_structure = call_claude(api_key, analysis_prompt)
                    else:
                        slide_structure = call_gemini(api_key, analysis_prompt)
                    
                    progress_bar.progress(35)
                    status_text.text(f"✅ Structure created: {len(slide_structure['slides'])} slides")
                    
                    # Show AI decisions
                    with st.expander("🤖 AI Layout Decisions"):
                        for slide in slide_structure['slides']:
                            if not slide.get('isTitle'):
                                st.write(f"**Slide {slide['slideNumber']}: {slide['title']}**")
                                st.write(f"- Layout: `{slide.get('layout', 'standard')}`")
                                st.write(f"- Reason: {slide.get('reasoning', 'N/A')}")
                                st.write("---")
                    
                    # Step 2: Generate code
                    status_text.text("💻 Building presentation...")
                    progress_bar.progress(60)
                    
                    js_code = generate_presentation_code(
                        slide_structure,
                        st.session_state.brand_config
                    )
                    
                    progress_bar.progress(75)
                    status_text.text("🎨 Rendering slides...")
                    
                    # Step 3: Execute
                    with tempfile.TemporaryDirectory() as temp_dir:
                        js_file = os.path.join(temp_dir, 'generate.js')
                        with open(js_file, 'w', encoding='utf-8') as f:
                            f.write(js_code)
                        
                        result = subprocess.run(
                            ['node', js_file],
                            cwd=temp_dir,
                            capture_output=True,
                            text=True,
                            timeout=90
                        )
                        
                        if result.returncode != 0:
                            st.error(f"❌ Error: {result.stderr}")
                        else:
                            output_file = os.path.join(temp_dir, 'output.pptx')
                            
                            if os.path.exists(output_file):
                                with open(output_file, 'rb') as f:
                                    pptx_data = f.read()
                                
                                progress_bar.progress(100)
                                status_text.text("✅ Presentation ready!")
                                
                                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                                st.markdown(f"""
                                ### ✅ Success!
                                - 🤖 **AI Used:** {ai_provider}
                                - 🎨 **Branding:** {st.session_state.brand_config['company_name']}
                                - 📊 **Slides:** {len(slide_structure['slides'])} total
                                """)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                filename = f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
                                
                                st.download_button(
                                    label="📥 Download Presentation",
                                    data=pptx_data,
                                    file_name=filename,
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                    use_container_width=True
                                )
                            else:
                                st.error("❌ File not created. Try again.")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def call_claude(api_key, prompt):
    """Call Anthropic Claude API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            return json.loads(response_text)
    except Exception as e:
        st.error(f"Claude API Error: {str(e)}")
        raise


def call_gemini(api_key, prompt):
    """Call Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        response_text = response.text
        
        # Parse JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            return json.loads(response_text)
    except Exception as e:
        st.error(f"Gemini API Error: {str(e)}")
        raise


def generate_presentation_code(slide_structure, brand_config):
    """Generate JavaScript code (same as before)"""
    
    js_code = f"""const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = '{brand_config['company_name']}';

const colors = {{
  primary1: "{brand_config['colors']['yellow']}",
  primary2: "{brand_config['colors']['green']}",
  primary3: "{brand_config['colors']['teal']}",
  primary4: "{brand_config['colors']['blue']}",
  accent1: "{brand_config['colors']['coral']}",
  accent2: "{brand_config['colors']['purple']}",
  background: "{brand_config['colors']['cream']}",
  textDark: "{brand_config['colors']['darkText']}",
  textLight: "{brand_config['colors']['lightText']}",
  white: "{brand_config['colors']['white']}"
}};

const brandConfig = {{
  companyName: {json.dumps(brand_config['company_name'])},
  tagline1: {json.dumps(brand_config['tagline_1'])},
  tagline2: {json.dumps(brand_config['tagline_2'])},
  hashtag: {json.dumps(brand_config['hashtag'])},
  footerText: {json.dumps(brand_config['footer_text'])},
  font: "{brand_config['font']}"
}};

function addBrandHeader(slide) {{
  slide.addText(brandConfig.companyName, {{
    x: 0.5, y: 0.3, w: 2, h: 0.4,
    fontSize: 16, bold: true, color: colors.textDark, fontFace: brandConfig.font
  }});
  slide.addText(brandConfig.tagline1, {{
    x: 2.6, y: 0.3, w: 5, h: 0.4,
    fontSize: 9, color: colors.textLight, fontFace: brandConfig.font
  }});
  slide.addText(brandConfig.tagline2, {{
    x: 2.6, y: 0.55, w: 5, h: 0.3,
    fontSize: 8, color: colors.textLight, fontFace: brandConfig.font
  }});
  slide.addText(brandConfig.hashtag, {{
    x: 8.5, y: 0.3, w: 1, h: 0.4,
    fontSize: 9, color: colors.textLight, fontFace: brandConfig.font, align: "right"
  }});
}}

function addBrandFooter(slide) {{
  slide.addText(brandConfig.footerText, {{
    x: 0.5, y: 5.2, w: 9, h: 0.2,
    fontSize: 8, color: colors.textLight, fontFace: brandConfig.font, align: "center"
  }});
}}

// [Layout functions - same as previous implementation]
// Including: definition_boxes, split_layout, icon_grid, numbered_boxes, 
// comparison_table, flow_diagram, three_boxes

"""
    
    # Add all layout functions (keeping code concise here)
    js_code += get_layout_functions_compact()
    
    # Generate slides
    js_code += "\n// Generate Slides\n"
    
    for slide in slide_structure['slides']:
        if slide.get('isTitle'):
            js_code += f"""
let slide{slide['slideNumber']} = pres.addSlide();
slide{slide['slideNumber']}.background = {{ color: colors.background }};
addBrandHeader(slide{slide['slideNumber']});
slide{slide['slideNumber']}.addText({json.dumps(slide['title'])}, {{
  x: 0.5, y: 2, w: 9, h: 1, fontSize: 48, bold: true, 
  color: colors.textDark, fontFace: brandConfig.font, align: "center", valign: "middle"
}});
"""
            if 'subtitle' in slide:
                js_code += f"""
slide{slide['slideNumber']}.addText({json.dumps(slide['subtitle'])}, {{
  x: 0.5, y: 3.2, w: 9, h: 0.5, fontSize: 20, 
  color: colors.textLight, fontFace: brandConfig.font, align: "center", italic: true
}});
"""
            js_code += f"addBrandFooter(slide{slide['slideNumber']});\n"
        else:
            layout_type = slide.get('layout', 'numbered_boxes')
            js_code += f"\ncreate_{layout_type}(pres, {json.dumps(slide['title'])}, {json.dumps(slide['content'])});\n"
    
    js_code += """
pres.writeFile({ fileName: "output.pptx" });
console.log("Success!");
"""
    
    return js_code


def get_layout_functions_compact():
    """Compact version of layout functions"""
    # This would include all the layout functions from the previous version
    # Keeping compact for brevity - same implementation as edubridge_ppt_generator.py
    return """
function create_numbered_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4];(c.boxes||[]).slice(0,4).forEach((b,i)=>{const x=.5+i*2.3;s.addShape(p.shapes.RECTANGLE,{x,y:2.2,w:2.1,h:2.4,fill:{color:cols[i]}});s.addText(String(i+1).padStart(2,'0'),{x,y:2.3,w:2.1,h:.8,fontSize:72,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"top"});s.addText(b,{x:x+.15,y:3.3,w:1.8,h:1.1,fontSize:16,bold:true,color:colors.white,fontFace:brandConfig.font,align:"left",valign:"top"})});addBrandFooter(s)}
function create_definition_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});s.addShape(p.shapes.RECTANGLE,{x:1,y:1.9,w:8,h:1.2,fill:{color:colors.white}});s.addShape(p.shapes.RECTANGLE,{x:1,y:1.9,w:.08,h:1.2,fill:{color:colors.primary3}});s.addText(c.definition||"",{x:1.3,y:2.05,w:7.4,h:1,fontSize:14,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"});const cols=[colors.primary1,colors.primary2,colors.primary4];(c.boxes||[]).slice(0,3).forEach((b,i)=>{const x=1+i*2.7;s.addShape(p.shapes.RECTANGLE,{x,y:3.4,w:2.4,h:1,fill:{color:cols[i]}});s.addText(b,{x:x+.15,y:3.5,w:2.1,h:.8,fontSize:13,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"})});addBrandFooter(s)}
function create_split_layout(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:28,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});(c.bullets||[]).slice(0,5).forEach((b,i)=>{s.addShape(p.shapes.OVAL,{x:.7,y:2+i*.6,w:.15,h:.15,fill:{color:colors.primary3}});s.addText(b,{x:1,y:1.95+i*.6,w:4.5,h:.5,fontSize:11,color:colors.textDark,fontFace:brandConfig.font})});const hcols=[colors.primary2,colors.primary4,colors.accent1];(c.highlights||[]).slice(0,3).forEach((h,i)=>{const y=2+i*1;s.addShape(p.shapes.RECTANGLE,{x:5.8,y,w:3.5,h:.8,fill:{color:hcols[i]}});s.addText(h,{x:6,y:y+.1,w:3.3,h:.6,fontSize:14,bold:true,color:colors.white,fontFace:brandConfig.font,valign:"middle"})});addBrandFooter(s)}
function create_icon_grid(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4,colors.accent1,colors.accent2];(c.items||[]).slice(0,6).forEach((item,i)=>{const col=i%3,row=Math.floor(i/3),x=1.2+col*2.7,y=2.3+row*1.5;s.addShape(p.shapes.RECTANGLE,{x,y,w:2.4,h:1.2,fill:{color:colors.white},line:{color:cols[i%6],width:3}});s.addShape(p.shapes.OVAL,{x:x+.85,y:y+.15,w:.7,h:.7,fill:{color:cols[i%6]}});s.addText(item.icon||"✓",{x:x+.85,y:y+.15,w:.7,h:.7,fontSize:24,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});s.addText(item.text||item,{x:x+.1,y:y+.7,w:2.2,h:.4,fontSize:11,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"})});addBrandFooter(s)}
function create_comparison_table(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});s.addShape(p.shapes.OVAL,{x:4.6,y:2.3,w:.8,h:.8,fill:{color:colors.accent1}});s.addText("VS",{x:4.6,y:2.3,w:.8,h:.8,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});s.addShape(p.shapes.RECTANGLE,{x:.7,y:1.9,w:3.7,h:.5,fill:{color:colors.primary4}});s.addText(c.left_title||"A",{x:.7,y:1.9,w:3.7,h:.5,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});(c.left_points||[]).slice(0,3).forEach((pt,i)=>{s.addShape(p.shapes.RECTANGLE,{x:.7,y:2.5+i*.5,w:3.7,h:.4,fill:{color:colors.white},line:{color:colors.primary4,width:2}});s.addText(pt,{x:.85,y:2.55+i*.5,w:3.4,h:.3,fontSize:11,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"})});s.addShape(p.shapes.RECTANGLE,{x:5.6,y:1.9,w:3.7,h:.5,fill:{color:colors.primary2}});s.addText(c.right_title||"B",{x:5.6,y:1.9,w:3.7,h:.5,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});(c.right_points||[]).slice(0,3).forEach((pt,i)=>{s.addShape(p.shapes.RECTANGLE,{x:5.6,y:2.5+i*.5,w:3.7,h:.4,fill:{color:colors.white},line:{color:colors.primary2,width:2}});s.addText(pt,{x:5.75,y:2.55+i*.5,w:3.4,h:.3,fontSize:11,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"})});addBrandFooter(s)}
function create_flow_diagram(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4];(c.steps||[]).slice(0,4).forEach((step,i)=>{const x=.8+i*2.3;s.addShape(p.shapes.RECTANGLE,{x,y:2.5,w:2,h:.8,fill:{color:cols[i]}});s.addText(step,{x:x+.1,y:2.6,w:1.8,h:.6,fontSize:12,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});if(i<3)s.addShape(p.shapes.RIGHT_ARROW,{x:x+2.1,y:2.7,w:.7,h:.4,fill:{color:colors.textLight}})});if(c.outcome){s.addShape(p.shapes.RECTANGLE,{x:1,y:4,w:8,h:.6,fill:{color:colors.accent1}});s.addText("🎯 "+c.outcome,{x:1.2,y:4.1,w:7.6,h:.4,fontSize:13,bold:true,color:colors.white,fontFace:brandConfig.font,valign:"middle"})}addBrandFooter(s)}
function create_three_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary4];(c.boxes||[]).slice(0,3).forEach((b,i)=>{const x=1+i*2.7;s.addShape(p.shapes.RECTANGLE,{x,y:2.5,w:2.4,h:1.5,fill:{color:cols[i]}});s.addText(b,{x:x+.2,y:2.7,w:2,h:1.1,fontSize:14,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"})});addBrandFooter(s)}
"""


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.9rem;'>
    <p>🎓 EduBridge AI PPT Generator | Multi-AI Support</p>
    <p>Powered by Claude & Gemini</p>
</div>
""", unsafe_allow_html=True)
