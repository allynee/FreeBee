// node index.js
const cors = require("cors");
const express = require("express");
const expressGraphQL = require("express-graphql").graphqlHTTP;
const {
  GraphQLSchema,
  GraphQLObjectType,
  GraphQLString,
  GraphQLNonNull,
} = require("graphql");

const geocoding = require("./geocoding");

const app = express();
app.use(cors());
const AddressType = new GraphQLObjectType({
  name: "Address",
  fields: () => ({
    code: { type: GraphQLString },
    address: { type: GraphQLString },
    postal_code: { type: GraphQLString },
    area: { type: GraphQLString },
    district: { type: GraphQLString },
  }),
});

const RootQueryType = new GraphQLObjectType({
  name: "Query",
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
    return "Hello world!";
  },
};

const schema = new GraphQLSchema({
  query: RootQueryType,
});

// const getAddressData = async (address) => {
//   const response = await fetch(`/graphql/${address}`, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ query: `{ address(address: "${address}") { address, postal_code, area, district } }` }),
//   });
//   const { data } = await response.json();
//   return data.address;
// }
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

app.use(
  "/graphql",
  expressGraphQL({
    schema: schema,
    graphiql: true,
    rootValue: root,
  })
);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
