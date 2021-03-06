import os

from google.cloud import speech
#import io

import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secretkey.json'

def transcribe_file(content, lang='英語'):
    lang_code={
        '英語': 'en-US',
        '日本語': 'ja-JP',
        'スペイン語': 'es-ES'
    }

    client = speech.SpeechClient()

#    with io.open(speech_file, 'rb') as f:
#        content=f.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code=lang_code[lang]
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        st.write(result.alternatives[0].transcript)
#        print("認識結果: {}".format(result.alternatives[0].transcript))

st.title('音声文字起こしアプリ')
st.header('概要')
st.write('こちらは音声ファイルを読み込んで文字起こしができるアプリです。音声認識AIを搭載したGoogle Cloud Speech-to-Textを利用しています。リンクは下記です。')
st.markdown('<a href="https://cloud.google.com/speech-to-text">Cloud Speech-to-Text</a>', unsafe_allow_html=True)

upload_file=st.file_uploader('ファイルのアップロード',type={'mp3','wav'})
if upload_file is not None:
    content = upload_file.read()
    st.subheader('ファイル詳細')
    file_details = {'FileName': upload_file.name, 'FileType': upload_file.type, 'FileSize': upload_file.size}
    st.write(file_details)
    st.subheader('音声の再生')
    st.audio(content)
    
    st.subheader('言語選択')
    option = st.selectbox('翻訳言語を選択してください',
                         ('英語', '日本語', 'スペイン語'))
    st.write('選択中の言語：', option)
    
    st.write('文字起こし')
    if st.button('開始'):
        comment = st.empty()
        comment.write('文字起こしを開始します')
        transcribe_file(content, lang=option)
        comment.write('完了しました')
