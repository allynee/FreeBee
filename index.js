const express = require('express');
const expressGraphQL = require('express-graphql').graphqlHTTP;
const {
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLString,
    GraphQLList,
    GraphQLInt,
    GraphQLNonNull,
} = require('graphql');
const app = express();

const schema = new GraphQLSchema({
    query: new GraphQLObjectType({
        name: 'Query',
        fields: () => ({
            message: { 
                type: GraphQLString,
                resolve: () => 'Hello World' 
            }
        })
    })
});

app.use('/graphql', expressGraphQL({
    schema: schema,
    graphiql: true
}))
app.listen(5000., () => console.log('Server started on port 5000'));