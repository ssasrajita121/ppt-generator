import streamlit as st
import subprocess
import tempfile
import os
import json
import re
from datetime import datetime
import shutil
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(page_title="EduBridge AI PPT Generator", page_icon="📊", layout="wide")

# CSS
st.markdown("""<style>.main-header{font-size:2.5rem;font-weight:bold;color:#2D3748;text-align:center;margin-bottom:0.5rem}.stButton>button{background-color:#4299E1;color:white;font-size:1.1rem;padding:0.75rem 2rem;border-radius:0.5rem}</style>""", unsafe_allow_html=True)

# Brand config
if 'brand_config' not in st.session_state:
    st.session_state.brand_config = {
        'company_name': 'EduBridge',
        'tagline_1': "India's leading Workforce Development Platform that helps learners in building careers",
        'tagline_2': "with leading corporates through training & other career building services.",
        'hashtag': '#letslearntoearn',
        'footer_text': 'All rights reserved.',
        'colors': {'yellow': 'F9D54A', 'green': '4EDA3B', 'teal': '2DD4BF', 'blue': '5B9FD8',
                   'coral': 'F96167', 'purple': '9D4EDD', 'cream': 'F5E6D3',
                   'darkText': '2D3748', 'lightText': '718096', 'white': 'FFFFFF'},
        'font': 'Calibri'
    }

# Get API key from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

def call_gemini(prompt):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        return json.loads(json_match.group()) if json_match else json.loads(response.text)
    except Exception as e:
        st.error(f"Gemini Error: {str(e)}")
        raise

def get_layout_functions():
    return """
function extractText(obj){let text='';if(typeof obj==='string')text=obj;else if(typeof obj==='object'&&obj!==null)text=obj.text||obj.title||obj.name||obj.description||obj.content||JSON.stringify(obj);else text=String(obj);text=text.replace(/\*\*(.+?)\*\*/g,'$1').replace(/\*(.+?)\*/g,'$1').replace(/`(.+?)`/g,'$1').replace(/\*\*/g,'').replace(/\*/g,'');return text.trim()}
function create_numbered_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4];const boxes=c.boxes||[];boxes.slice(0,4).forEach((b,i)=>{const x=.5+i*2.3;s.addShape(p.shapes.RECTANGLE,{x,y:2.2,w:2.1,h:2.4,fill:{color:cols[i]}});s.addText(String(i+1).padStart(2,'0'),{x,y:2.3,w:2.1,h:.8,fontSize:72,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"top"});s.addText(extractText(b),{x:x+.15,y:3.3,w:1.8,h:1.1,fontSize:16,bold:true,color:colors.white,fontFace:brandConfig.font,align:"left",valign:"top"})});addBrandFooter(s)}
function create_definition_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});s.addShape(p.shapes.RECTANGLE,{x:1,y:1.9,w:8,h:1.2,fill:{color:colors.white}});s.addShape(p.shapes.RECTANGLE,{x:1,y:1.9,w:.08,h:1.2,fill:{color:colors.primary3}});s.addText(extractText(c.definition||""),{x:1.3,y:2.05,w:7.4,h:1,fontSize:14,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"});const cols=[colors.primary1,colors.primary2,colors.primary4];const boxes=c.boxes||[];boxes.slice(0,3).forEach((b,i)=>{const x=1+i*2.7;s.addShape(p.shapes.RECTANGLE,{x,y:3.4,w:2.4,h:1,fill:{color:cols[i]}});s.addText(extractText(b),{x:x+.15,y:3.5,w:2.1,h:.8,fontSize:13,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"})});addBrandFooter(s)}
function create_split_layout(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:28,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const bullets=c.bullets||[];bullets.slice(0,5).forEach((b,i)=>{s.addShape(p.shapes.OVAL,{x:.7,y:2+i*.6,w:.15,h:.15,fill:{color:colors.primary3}});s.addText(extractText(b),{x:1,y:1.95+i*.6,w:4.5,h:.5,fontSize:11,color:colors.textDark,fontFace:brandConfig.font})});const hcols=[colors.primary2,colors.primary4,colors.accent1];const highlights=c.highlights||[];highlights.slice(0,3).forEach((h,i)=>{const y=2+i*1;s.addShape(p.shapes.RECTANGLE,{x:5.8,y,w:3.5,h:.8,fill:{color:hcols[i]}});s.addText(extractText(h),{x:6,y:y+.1,w:3.3,h:.6,fontSize:14,bold:true,color:colors.white,fontFace:brandConfig.font,valign:"middle"})});addBrandFooter(s)}
function create_icon_grid(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4,colors.accent1,colors.accent2];const items=c.items||[];items.slice(0,6).forEach((item,i)=>{const col=i%3,row=Math.floor(i/3),x=1.2+col*2.7,y=2.3+row*1.5;s.addShape(p.shapes.RECTANGLE,{x,y,w:2.4,h:1.2,fill:{color:colors.white},line:{color:cols[i%6],width:3}});s.addShape(p.shapes.OVAL,{x:x+.85,y:y+.15,w:.7,h:.7,fill:{color:cols[i%6]}});const icon=typeof item==='object'?item.icon||"✓":"✓";s.addText(String(icon),{x:x+.85,y:y+.15,w:.7,h:.7,fontSize:24,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});s.addText(extractText(item),{x:x+.1,y:y+.7,w:2.2,h:.4,fontSize:11,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"})});addBrandFooter(s)}
function create_comparison_table(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});s.addShape(p.shapes.OVAL,{x:4.6,y:2.3,w:.8,h:.8,fill:{color:colors.accent1}});s.addText("VS",{x:4.6,y:2.3,w:.8,h:.8,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});s.addShape(p.shapes.RECTANGLE,{x:.7,y:1.9,w:3.7,h:.5,fill:{color:colors.primary4}});s.addText(extractText(c.left_title||"A"),{x:.7,y:1.9,w:3.7,h:.5,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});const leftPts=c.left_points||[];leftPts.slice(0,3).forEach((pt,i)=>{s.addShape(p.shapes.RECTANGLE,{x:.7,y:2.5+i*.5,w:3.7,h:.4,fill:{color:colors.white},line:{color:colors.primary4,width:2}});s.addText(extractText(pt),{x:.85,y:2.55+i*.5,w:3.4,h:.3,fontSize:11,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"})});s.addShape(p.shapes.RECTANGLE,{x:5.6,y:1.9,w:3.7,h:.5,fill:{color:colors.primary2}});s.addText(extractText(c.right_title||"B"),{x:5.6,y:1.9,w:3.7,h:.5,fontSize:18,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});const rightPts=c.right_points||[];rightPts.slice(0,3).forEach((pt,i)=>{s.addShape(p.shapes.RECTANGLE,{x:5.6,y:2.5+i*.5,w:3.7,h:.4,fill:{color:colors.white},line:{color:colors.primary2,width:2}});s.addText(extractText(pt),{x:5.75,y:2.55+i*.5,w:3.4,h:.3,fontSize:11,color:colors.textDark,fontFace:brandConfig.font,valign:"middle"})});addBrandFooter(s)}
function create_flow_diagram(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary3,colors.primary4];const steps=c.steps||[];steps.slice(0,4).forEach((step,i)=>{const x=.8+i*2.3;s.addShape(p.shapes.RECTANGLE,{x,y:2.5,w:2,h:.8,fill:{color:cols[i]}});s.addText(extractText(step),{x:x+.1,y:2.6,w:1.8,h:.6,fontSize:12,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"});if(i<3)s.addShape(p.shapes.RIGHT_ARROW,{x:x+2.1,y:2.7,w:.7,h:.4,fill:{color:colors.textLight}})});if(c.outcome){s.addShape(p.shapes.RECTANGLE,{x:1,y:4,w:8,h:.6,fill:{color:colors.accent1}});s.addText("🎯 "+extractText(c.outcome),{x:1.2,y:4.1,w:7.6,h:.4,fontSize:13,bold:true,color:colors.white,fontFace:brandConfig.font,valign:"middle"})}addBrandFooter(s)}
function create_three_boxes(p,t,c){let s=p.addSlide();s.background={color:colors.background};addBrandHeader(s);s.addText(t,{x:.5,y:1.1,w:9,h:.5,fontSize:32,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:"center"});const cols=[colors.primary1,colors.primary2,colors.primary4];const boxes=c.boxes||[];boxes.slice(0,3).forEach((b,i)=>{const x=1+i*2.7;s.addShape(p.shapes.RECTANGLE,{x,y:2.5,w:2.4,h:1.5,fill:{color:cols[i]}});s.addText(extractText(b),{x:x+.2,y:2.7,w:2,h:1.1,fontSize:14,bold:true,color:colors.white,fontFace:brandConfig.font,align:"center",valign:"middle"})});addBrandFooter(s)}
"""

def generate_code(slide_structure, brand_config):
    js = f"""const pptxgen=require("pptxgenjs");let pres=new pptxgen();pres.layout='LAYOUT_16x9';pres.author='{brand_config['company_name']}';
const colors={{primary1:"{brand_config['colors']['yellow']}",primary2:"{brand_config['colors']['green']}",primary3:"{brand_config['colors']['teal']}",primary4:"{brand_config['colors']['blue']}",accent1:"{brand_config['colors']['coral']}",accent2:"{brand_config['colors']['purple']}",background:"{brand_config['colors']['cream']}",textDark:"{brand_config['colors']['darkText']}",textLight:"{brand_config['colors']['lightText']}",white:"{brand_config['colors']['white']}"}};
const brandConfig={{companyName:{json.dumps(brand_config['company_name'])},tagline1:{json.dumps(brand_config['tagline_1'])},tagline2:{json.dumps(brand_config['tagline_2'])},hashtag:{json.dumps(brand_config['hashtag'])},footerText:{json.dumps(brand_config['footer_text'])},font:"{brand_config['font']}"}};
function addBrandHeader(s){{s.addText(brandConfig.companyName,{{x:0.5,y:0.3,w:2,h:0.4,fontSize:16,bold:true,color:colors.textDark,fontFace:brandConfig.font}});s.addText(brandConfig.tagline1,{{x:2.6,y:0.3,w:5,h:0.4,fontSize:9,color:colors.textLight,fontFace:brandConfig.font}});s.addText(brandConfig.tagline2,{{x:2.6,y:0.55,w:5,h:0.3,fontSize:8,color:colors.textLight,fontFace:brandConfig.font}});s.addText(brandConfig.hashtag,{{x:8.5,y:0.3,w:1,h:0.4,fontSize:9,color:colors.textLight,fontFace:brandConfig.font,align:"right"}})}}
function addBrandFooter(s){{s.addText(brandConfig.footerText,{{x:0.5,y:5.2,w:9,h:0.2,fontSize:8,color:colors.textLight,fontFace:brandConfig.font,align:"center"}})}}
{get_layout_functions()}
"""
    for slide in slide_structure['slides']:
        if slide.get('isTitle'):
            js += f"let s{slide['slideNumber']}=pres.addSlide();s{slide['slideNumber']}.background={{color:colors.background}};addBrandHeader(s{slide['slideNumber']});s{slide['slideNumber']}.addText({json.dumps(slide['title'])},{{x:0.5,y:2,w:9,h:1,fontSize:48,bold:true,color:colors.textDark,fontFace:brandConfig.font,align:'center',valign:'middle'}});"
            if 'subtitle' in slide:
                js += f"s{slide['slideNumber']}.addText({json.dumps(slide['subtitle'])},{{x:0.5,y:3.2,w:9,h:0.5,fontSize:20,color:colors.textLight,fontFace:brandConfig.font,align:'center',italic:true}});"
            js += f"addBrandFooter(s{slide['slideNumber']});\n"
        else:
            layout = slide.get('layout', 'numbered_boxes')
            js += f"create_{layout}(pres,{json.dumps(slide['title'])},{json.dumps(slide['content'])});\n"
    js += 'pres.writeFile({fileName:"output.pptx"});console.log("Done!");'
    return js

# UI
st.markdown('<div class="main-header">🎓 EduBridge AI PPT Generator</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#718096;margin-bottom:2rem">Powered by Google Gemini AI</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### 📝 Presentation Details")
    topic = st.text_input("Topic *", placeholder="e.g., AI Agents, Java OOP")
    slide_count = st.slider("Content Slides", 3, 10, 5)
    instructions = st.text_area("Instructions (Optional)", height=100)

with col2:
    st.info(f"**Slides:** {slide_count + 1}\n**AI:** Gemini 2.5 Flash\n**Format:** 16:9")

st.markdown("---")

if st.button("🚀 Generate Presentation", use_container_width=True):
    if not GOOGLE_API_KEY:
        st.error("⚠️ GOOGLE_API_KEY not found. Set in environment or Streamlit secrets.")
    elif not topic:
        st.error("⚠️ Please enter a topic")
    else:
        try:
            progress = st.progress(0)
            status = st.empty()
            status.text("🧠 AI analyzing...")
            progress.progress(20)
            
            prompt = f"""Generate {slide_count + 1} slides on "{topic}". {instructions if instructions else ''}
Return ONLY JSON. NO markdown (**bold** *italic* `code`). Keep text SHORT (max 15 words per box).
{{"slides":[{{"slideNumber":1,"title":"Title","isTitle":true}},{{"slideNumber":2,"title":"Slide","layout":"numbered_boxes","content":{{"boxes":["text1","text2","text3","text4"]}}}}]}}
Layouts: definition_boxes, split_layout, icon_grid, numbered_boxes, comparison_table, flow_diagram, three_boxes"""
            
            slide_data = call_gemini(prompt)
            progress.progress(60)
            status.text("💻 Building...")
            js_code = generate_code(slide_data, st.session_state.brand_config)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                node_src = os.path.join(os.getcwd(), 'node_modules')
                if os.path.exists(node_src):
                    shutil.copytree(node_src, os.path.join(temp_dir, 'node_modules'))
                with open(os.path.join(temp_dir, 'gen.js'), 'w', encoding='utf-8') as f:
                    f.write(js_code)
                result = subprocess.run(['node', 'gen.js'], cwd=temp_dir, capture_output=True, text=True, timeout=90)
                
                if result.returncode == 0:
                    with open(os.path.join(temp_dir, 'output.pptx'), 'rb') as f:
                        pptx_data = f.read()
                    progress.progress(100)
                    status.text("✅ Done!")
                    st.success("✅ Generated successfully!")
                    st.download_button("📥 Download", pptx_data, f"{topic.replace(' ', '_')}.pptx",
                                      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                      use_container_width=True)
                else:
                    st.error(f"❌ {result.stderr}")
        except Exception as e:
            st.error(f"❌ {str(e)}")

st.markdown("---")
st.markdown('<div style="text-align:center;color:#718096">🎓 EduBridge | Powered by Google Gemini</div>', unsafe_allow_html=True)
