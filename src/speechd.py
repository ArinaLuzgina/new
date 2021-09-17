import speechd

tts_d = speechd.SSIPClient('test')

tts_d.set_output_module('Festival')

tts_d.set_language('ru')

tts_d.speak('И нежный вкус родимой речи так чисто губы холодит')

tts_d.close()