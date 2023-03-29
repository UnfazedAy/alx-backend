import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

// Redis set-up
const client = createClient();
client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', (err) => console.log('Redis client not connected to the server: ', err));

// Express set-up
const port = 1245;
const hostname = '0.0.0.0';
const app = express();

const listProducts = [
  { 'itemId': 1, 'itemName': 'Suitcase 250', 'price': 50, 'initialAvailableQuantity': 4 },
  { 'itemId': 2, 'itemName': 'Suitcase 450', 'price': 100, 'initialAvailableQuantity': 10 },
  { 'itemId': 3, 'itemName': 'Suitcase 650', 'price': 350, 'initialAvailableQuantity': 2 },
  { 'itemId': 4, 'itemName': 'Suitcase 1050', 'price': 550, 'initialAvailableQuantity': 5 }
];

function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  const getAsync = promisify(client.get).bind(client);
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

  const reservedStock = await getCurrentReservedStockById(itemId);

   // This is needed because I need to use the getCurrentReservedStockById function
  const stock = {
    itemId: item.itemId,
    itemName: item.itemName,
    price: item.price,
    initialAvailableQuantity: item.initialAvailableQuantity,
    currentQuantity: item.initialAvailableQuantity - (parseInt(reservedStock) || 0)
  }
  res.status(404);
  res.json(stock);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(parseInt(itemId));

  if (item) {
    // if items available is less than 1 
    if (item.initialAvailableQuantity < 1) {
      res.json({"status":"Not enough stock available","itemId":itemId});
    } else {
      // reserves 1 item if item available is greater than 1
      reserveStockById(itemId, 1);
      res.json({"status":"Reservation confirmed","itemId": itemId});
    }
  } else {
    // If item doesn't exist
    res.json({"status":"Product not found"})
  }
});
  

app.listen(port, hostname, () => console.log(`Server running on http://${hostname}:${port}`));
