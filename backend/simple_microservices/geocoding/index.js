const express = require("express");
const expressGraphQL = require("express-graphql").graphqlHTTP;
const { 
  GraphQLSchema,
  GraphQLObjectType,
  GraphQLString,
  GraphQLNonNull
 } = require("graphql");

const geocoding = require('./geocoding');

const app = express();

const AddressType = new GraphQLObjectType({
  name: 'Address',
  fields: () => ({
    address: { type: GraphQLString },
    postal_code: { type: GraphQLString },
    area: { type: GraphQLString },
    district: { type: GraphQLString },
  }),
});

const RootQueryType = new GraphQLObjectType({
  name: 'Query',
  fields: () => ({
    address: {
      type: AddressType,
      args: {
        address: { type: GraphQLString },
      },
      resolve: async (_, { address }) => {
        const geocodeResult = await geocoding.geocode(address);
        return geocodeResult;
      },
    },
  }),
});

var root = {
  hello: () => {
    return 'Hello world!';
  },
};

const schema = new GraphQLSchema({
  query: RootQueryType,
});

const getAddressData = async (address) => {
  const response = await fetch(`/graphql/${address}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: `{ address(address: "${address}") { address, postal_code, area, district } }` }),
  });
  const { data } = await response.json();
  return data.address;
}
// const schema = new GraphQLSchema({
//   query: new GraphQLObjectType({
//     name: 'Query',
//     fields: () => ({
//       address: {
//         type: new GraphQLObjectType({
//           name: 'Address',
//           fields: () => ({
//             address: { type: GraphQLString },
//             postalCode: { type: GraphQLString },
//             area: { type: GraphQLString },
//             district: { type: GraphQLString },
//             geometry: { type: GraphQLString },
//           }),
//         }),
//         args: {
//           address: { type: GraphQLNonNull(GraphQLString) },
//         },
//         resolve: async (_, args) => {
//           const address = args.address;
//           const addressResult = await getAddressData(address);
//           return addressResult;
//         },
//       },
//     }),
//   }),
// });
const port = 3000;
// const axios = require("axios");

// app.get("/:address", async (req, res) => {
//   const address = req.params.address;
//   const geocodeResult = await geocoding.geocode(address);
//   res.json(geocodeResult);
// });
app.use('/graphql', expressGraphQL({
  schema: schema,
  graphiql: true,
  rootValue: root,
}));
// app.post('/graphql', express.json(), async (req, res) => {
//   const { query } = "123";
//   const result = await expressGraphQL(schema, query);
//   res.send(result);
// });


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
