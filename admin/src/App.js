import drfProvider from 'ra-data-django-rest-framework';
import React from 'react';
import { Admin, EditGuesser, fetchUtils, Resource } from 'react-admin';
import authProviderDjango from './authProvider';
import { ExtractorCreate, ExtractorList, ExtractorShow } from './extractor';
import { Layout } from './layout';
import { LighthouseCreate, LighthouseList, LighthouseShow } from './lighthouse';
import {  LighthouseResultsList, LighthouseResultsShow } from './lighthouseResults';
import { WebsiteList } from './website';
import { YakeList } from './yake'
import { Dashboard } from './dashboard/Dashboard'


const fetchJson = (url, options = {}) => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    const { key } = JSON.parse(localStorage.getItem('auth'));
    options.headers.set('Authorization', `Token ${key}`);
    return fetchUtils.fetchJson(url, options);
}


const App = () => (
    <Admin layout={Layout} dashboard={Dashboard} authProvider={authProviderDjango} dataProvider={drfProvider('http://localhost:8000/api', fetchJson)}>
        <Resource name="website_user" options={{ label: 'Websites' }}  list={WebsiteList}/>
        <Resource name="extractor" list={ExtractorList} edit={EditGuesser} create={ExtractorCreate} show={ExtractorShow}/>
        <Resource name="lighthouse" title="Lighthouse" options={{ title: 'lighthouse', label: 'Lighthouse' }} list={LighthouseList} show={LighthouseShow}  edit={EditGuesser} create={LighthouseCreate}/>
        <Resource name="lighthouse_details" title="Lighthouse" options={{ title: 'lighthouse', label: 'Lighthouse Results' }} list={LighthouseResultsList} show={LighthouseResultsShow} />
        <Resource name="keywords/yake" options={{ label: 'Yake' }}  list={YakeList}/>
    </Admin>
);

export default App;