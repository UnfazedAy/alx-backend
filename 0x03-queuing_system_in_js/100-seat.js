import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

// Redis set up
const client = createClient();
client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', (err) => console.log('Redis client not connected to the server: ', err));

// kue set-up
const queue = createQueue();

// express set-up
const app = express();
const port = 1245;
const hostname = '0.0.0.0';

let reservationEnabled = true;

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const getAsync = promisify(client.get).bind(client);
  try {
    const value = await getAsync('available_seats');
    return value;
  } catch (err) {
    throw err;
  }
}

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({"numberOfAvailableSeats":availableSeats});
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled === false) {
    res.json({ "status": "Reservation are blocked" });
  }

  const job = queue.create('reserve_seat');
  job.save((err) => {
    if (!err) res.json({ "status": "Reservation in process" });
    res.json({ "status": "Reservation failed" });
  });

  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`));
});

app.get('/process', (req, res) => {
  res.json({ "status": "Queue processing" });
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    const currentSeat = (parseInt(availableSeats) || 0) - 1;
    reserveSeat(currentSeat);

    if (currentSeat === 0) reservationEnabled = false;
    else if (currentSeat > 0) done();
    done(new Error('Not enough seats available'));

  });
});

app.listen(port, hostname, () => {
  reserveSeat(50);
  console.log(`Server running on http://${hostname}:${port}`);
});
