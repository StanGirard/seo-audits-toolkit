import React from 'react';
import { Admin, Resource, ListGuesser, EditGuesser } from 'react-admin';
import drfProvider, { tokenAuthProvider, fetchJsonWithAuthToken } from 'ra-data-django-rest-framework';
import {ExtractorList , ExtractorCreate, ExtractorShow}  from './extractor';
import { Layout } from './layout';
const authProvider = tokenAuthProvider()




const App = () => (
    <Admin layout={Layout} dataProvider={drfProvider('http://localhost:8000/api', fetchJsonWithAuthToken)}>
        <Resource name="extractor" list={ExtractorList} edit={EditGuesser} create={ExtractorCreate} show={ExtractorShow}/>
    </Admin>
);

export default App;