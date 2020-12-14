import React from 'react';
import { Admin, Resource, ListGuesser, EditGuesser } from 'react-admin';
import drfProvider, { tokenAuthProvider, fetchJsonWithAuthToken } from 'ra-data-django-rest-framework';
const authProvider = tokenAuthProvider()
const App = () => (
    <Admin dataProvider={drfProvider('http://localhost:8000', fetchJsonWithAuthToken)}>
        <Resource name="extractor" list={ListGuesser} edit={EditGuesser} />
    </Admin>
);

export default App;