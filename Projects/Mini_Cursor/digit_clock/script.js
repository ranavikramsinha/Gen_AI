function updateClock() {
    const now = new Date();

    const options = { weekday: 'long' };
    const day = now.toLocaleDateString('en-US', options);
    const date = now.getDate();
    const month = now.toLocaleString('default', { month: 'long' });
    const year = now.getFullYear();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    // Format time as two digits
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    document.getElementById('time').textContent = `${hours}:${minutes}:${seconds}`;
    document.getElementById('day').textContent = day;
    document.getElementById('date').textContent = `Date: ${date}`;
    document.getElementById('month').textContent = `Month: ${month}`;
    document.getElementById('year').textContent = `Year: ${year}`;
}

setInterval(updateClock, 1000);
updateClock();