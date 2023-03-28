import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

// Redis set-up
const client = createClient();
const getAsync = promisify(client.get).bind(client);
client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', (err) => console.log('Redis client not connected to the server: ', err));

// Express set-up
const port = 1245;
const hostname = '0.0.0.0';
const app = express();

const listProducts = [
  { 'itemId': 1, 'itemName': 'Suitcase 250', 'price': 50, 'initialAvailableQuantity': 4},
  { 'itemId': 2, 'itemName': 'Suitcase 450', 'price': 100, 'initialAvailableQuantity': 10},
  { 'itemId': 3, 'itemName': 'Suitcase 650', 'price': 350, 'initialAvailableQuantity': 2},
  { 'itemId': 4, 'itemName': 'Suitcase 1050', 'price': 550, 'initialAvailableQuantity': 5}
];

function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  try {
    const stock = await getAsync(itemId);
    return stock;
  } catch (err) {
    return;
  }
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId
  const item = getItemById(parseInt(itemId))

  if (!item) {
    res.json({"status":"Product not found"});
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  let output;

  if (currentStock === null) {
    output = item.initialAvailableQuantity;
  } else {
    output = parseInt(currentStock);
  }
   // This is needed because I need to use the getCurrentReservedStockById function
  const stock = {
    itemId: item.itemId,
    itemName: item.itemName,
    price: item.price,
    initialAvailableQuantity: item.initialAvailableQuantity,
    currentQuantity: output
  }
  res.json(stock);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (!item) {
    res.json({"status":"Product not found"});
    }

  const currentStock = await getCurrentReservedStockById(itemId);
  let output;

  if (currentStock !== null) {
    output = parseInt(currentStock);
    if (output > 0) {
      reserveStockById(itemId, output - 1);
      return res.json({"status": "Reservation confirmed", "itemId": itemId});
    } else {
      return res.json({"status": "Not enough stock available", "itemId": itemId});
    }
  }

  output = item.initialAvailableQuantity;
  reserveStockById(itemId, output - 1);
  return res.json({"status": "Reservation confirmed", "itemId": itemId});
});
  

app.listen(port, hostname, () => console.log(`Server running on http://${hostname}:${port}`));
