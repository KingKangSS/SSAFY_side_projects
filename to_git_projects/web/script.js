let timer;
let sec = 0;

function pad(val) { return val > 9 ? val : "0" + val; }

document.getElementById('startStopBtn').addEventListener('click', function() {
    if (this.textContent === "시작") {
        timer = setInterval(function(){
            document.getElementById("timer").textContent = pad(parseInt(sec / 3600, 10)) + ":" + pad(parseInt(sec / 60 % 60, 10)) + ":" + pad(sec % 60);
            sec++;
        }, 1000);
        this.textContent = "정지";
    } else {
        clearInterval(timer);
        this.textContent = "시작";
    }
});

document.getElementById('resetBtn').addEventListener('click', function() {
    sec = 0;
    document.getElementById("timer").textContent = "00:00:00";
    document.getElementById('startStopBtn').textContent = "시작";
    clearInterval(timer);
});

document.addEventListener('DOMContentLoaded', function() {
    fetchHangangTemperature();
});

function fetchHangangTemperature() {
    fetch('https://api.hangang.life/')
        .then(response => response.json())
        .then(data => {
            // API의 응답 구조에 맞춰 경로를 수정합니다.
            const noryangjinTemp = data.DATAs.DATA.HANGANG.노량진.TEMP;
            // '성공' 상태를 확인하는 대신, 데이터가 있는지 직접 확인합니다.
            if (noryangjinTemp !== undefined) {
                document.getElementById('hangang-temperature').textContent = `현재 한강의 온도는 ${noryangjinTemp}°C 입니다.`;
            } else {
                document.getElementById('hangang-temperature').textContent = '데이터를 불러오는데 실패했습니다.';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('hangang-temperature').textContent = '데이터를 불러오는 중 오류가 발생했습니다.';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    function updateExamCountdown() {
        const examDate = new Date('2024-03-04T09:00:00');
        const now = new Date();
        const diff = examDate - now;

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        const countdownElement = document.getElementById('exam-countdown');
        countdownElement.innerText = `IM 시험까지 ${days}일 ${hours}시간 ${minutes}분 ${seconds}초 남았습니다.`;

        // 1초마다 업데이트
        setTimeout(updateExamCountdown, 1000);
    }

    updateExamCountdown();
});
