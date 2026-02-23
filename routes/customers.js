const express = require('express');
const router = express.Router();

let customers = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];

router.get('/', (req, res) => {
  res.json(customers);
});

router.get('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const c = customers.find(x => x.id === id);
  if (!c) return res.status(404).json({ error: 'Customer not found' });
  res.json(c);
});

router.post('/', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) return res.status(400).json({ error: 'name and email required' });
  const id = customers.length ? Math.max(...customers.map(c => c.id)) + 1 : 1;
  const newCustomer = { id, name, email };
  customers.push(newCustomer);
  res.status(201).json(newCustomer);
});

router.put('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const index = customers.findIndex(x => x.id === id);
  if (index === -1) return res.status(404).json({ error: 'Customer not found' });
  const { name, email } = req.body;
  customers[index] = { id, name: name ?? customers[index].name, email: email ?? customers[index].email };
  res.json(customers[index]);
});

router.delete('/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const index = customers.findIndex(x => x.id === id);
  if (index === -1) return res.status(404).json({ error: 'Customer not found' });
  const removed = customers.splice(index, 1)[0];
  res.json(removed);
});

module.exports = router;
