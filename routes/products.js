const express = require('express');
const router = express.Router();

let products = [
  { id: 1, name: 'Widget', price: 9.99 },
  { id: 2, name: 'Gadget', price: 14.99 }
];

router.get('/', (req, res) => {
  res.json(products);
});

router.get('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const p = products.find(x => x.id === id);
  if (!p) return res.status(404).json({ error: 'Product not found' });
  res.json(p);
});

router.post('/', (req, res) => {
  const { name, price } = req.body;
  if (!name || price == null) return res.status(400).json({ error: 'name and price required' });
  const id = products.length ? Math.max(...products.map(p => p.id)) + 1 : 1;
  const newProduct = { id, name, price };
  products.push(newProduct);
  res.status(201).json(newProduct);
});

router.put('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const index = products.findIndex(x => x.id === id);
  if (index === -1) return res.status(404).json({ error: 'Product not found' });
  const { name, price } = req.body;
  products[index] = { id, name: name ?? products[index].name, price: price ?? products[index].price };
  res.json(products[index]);
});

router.delete('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const index = products.findIndex(x => x.id === id);
  if (index === -1) return res.status(404).json({ error: 'Product not found' });
  const removed = products.splice(index, 1)[0];
  res.json(removed);
});

module.exports = router;
