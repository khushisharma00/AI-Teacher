function speakLesson() {

    const lesson = document.getElementById("lesson");

    if (!lesson) return;

    const text = lesson.innerText.trim();

    if (text === "") return;

    const avatar = document.getElementById("teacherAvatar");

    speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 0.9;
    speech.pitch = 1;
    speech.volume = 1;

    function startSpeech(){

        const voices = speechSynthesis.getVoices();

        let voice =
            voices.find(v => v.name.includes("Samantha")) ||
            voices.find(v => v.name.includes("Karen")) ||
            voices.find(v => v.lang.startsWith("en"));

        if(voice){
            speech.voice = voice;
        }

        speech.onstart = function(){
            if(avatar){
                avatar.classList.add("speaking");
            }
        };

        speech.onend = function(){
            if(avatar){
                avatar.classList.remove("speaking");
            }
        };

        speechSynthesis.speak(speech);
    }

    if(speechSynthesis.getVoices().length===0){
        speechSynthesis.onvoiceschanged=startSpeech;
    }else{
        startSpeech();
    }
}