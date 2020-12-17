import React from 'react';
import { Admin, Resource, ListGuesser, EditGuesser } from 'react-admin';
import drfProvider, { tokenAuthProvider, fetchJsonWithAuthToken } from 'ra-data-django-rest-framework';
import {ExtractList , ExtractShow, PostShow}  from './extract';
const authProvider = tokenAuthProvider()



const App = () => (
    <Admin dataProvider={drfProvider('http://localhost:8000/api', fetchJsonWithAuthToken)}>
        <Resource name="extractor" list={ExtractList} />
    </Admin>
);

export default App;