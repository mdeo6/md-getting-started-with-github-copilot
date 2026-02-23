const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const productsRouter = require('./routes/products');
const customersRouter = require('./routes/customers');

app.use('/api/products', productsRouter);
app.use('/api/customers', customersRouter);

app.get('/', (req, res) => {
  res.send({ message: 'Express API running. Use /api/products or /api/customers' });
});

app.listen(port, () => {
  console.log(`Express API listening at http://localhost:${port}`);
});

module.exports = app;
