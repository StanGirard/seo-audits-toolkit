import React from 'react';
import { Admin,fetchUtils, Resource, ListGuesser, EditGuesser } from 'react-admin';
import drfProvider, { tokenAuthProvider, fetchJsonWithAuthToken } from 'ra-data-django-rest-framework';
import {ExtractorList , ExtractorCreate, ExtractorShow}  from './extractor';
import {WebsiteList} from './website'
import { Layout } from './layout';
import authProviderDjango from './authProvider'

// const httpClient = (url, options = {}) => {
//     if (!options.headers) {
//         options.headers = new Headers({ Accept: 'application/json' });
//     }
//     const { key } = JSON.parse(localStorage.getItem('auth'));
//     options.headers.set('Authorization', `Token ${key}`);
    
//     return fetchUtils.fetchJson(url, options);

// };

const fetchJson = (url, options = {}) => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    const { key } = JSON.parse(localStorage.getItem('auth'));
    options.headers.set('Authorization', `Token ${key}`);
    return fetchUtils.fetchJson(url, options);
}


const App = () => (
    <Admin layout={Layout} authProvider={authProviderDjango} dataProvider={drfProvider('http://localhost:8000/api', fetchJson)}>
        <Resource name="website_user" options={{ label: 'Websites' }}  list={WebsiteList}/>
        <Resource name="extractor" list={ExtractorList} edit={EditGuesser} create={ExtractorCreate} show={ExtractorShow}/>
        
    </Admin>
);

export default App;