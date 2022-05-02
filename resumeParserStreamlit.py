import base64
import tempfile
from resparser import resumeparser

import streamlit as st
from pdf2image import convert_from_path
import os,io
from google.cloud import vision_v1
import pandas as pd
from pathlib import Path

def show_pdf(file_path:str):
    """Show the PDF in Streamlit
    That returns as html component

    Parameters
    ----------
    file_path : [str]
        Uploaded PDF file path
    """

    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    """Streamlit application
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Projects\Resume\streamlit\vision_api\vision_api_key.json'
    client = vision_v1.ImageAnnotatorClient()

    st.title("Resume Parser")
    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    if uploaded_file is not None:
        # Make temp file path from uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            st.write(show_pdf(tmp_file.name))

            images = convert_from_path(tmp_file.name,500,fmt='png',poppler_path=r'C:\Projects\Resume\streamlit\poppler-0.68.0_x86\poppler-0.68.0\bin')
            print(type(images[0]))
            for i, image in enumerate(images):
                fname = 'image' + str(i) + '.png'
                image.save(fr'C:\Projects\Resume\streamlit\temp\{fname}', "PNG")
            abc = []
            for j in range(i + 1):

                with io.open(r'C:\Projects\Resume\streamlit\temp\image' + str(j) + '.png', 'rb') as image_file:
                    content = image_file.read()

                image = vision_v1.types.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations
                # print(texts)
                df = pd.DataFrame(columns=['locale', 'description'])
                for text in texts:
                    df = df.append(
                        dict(
                            locale=text.locale,
                            description=text.description
                        ),
                        ignore_index=True
                    )
                pdf_contents = df['description'][0]
                abc.append(pdf_contents)
                tesxt = abc[0].replace("\n", " ")
                # print(tesxt)
                entity = resumeparser(tesxt)

                print(entity)
                # print(pdf_contents)
                st.warning(entity)
            # pdf_contents = parser.from_file(path_to_pdf,service='text')



if __name__ == "__main__":
    main()

