import drfProvider from 'ra-data-django-rest-framework';
import React from 'react';
import { Admin, EditGuesser, fetchUtils, ListGuesser, Resource} from 'react-admin';
import authProviderDjango from './authProvider';
import { ExtractorCreate, ExtractorList, ExtractorShow, ExtractorEdit } from './extractor';
import { Layout } from './layout';
import { LighthouseCreate, LighthouseList, LighthouseShow, LighthouseEdit } from './lighthouse';
import {  LighthouseResultsList, LighthouseResultsShow } from './lighthouseResults';
import { WebsiteList } from './website';
import { YakeList, YakeShow, YakeCreate, yakeEdit } from './yake'
import { SitemapList, SitemapShow, SitemapCreate, SitemapEdit } from './sitemap'
import { Dashboard } from './dashboard/Dashboard'
import { BertCreate, BertList, BertShow, BertEdit } from './bert';
import { SecurityCreate, SecurityList, SecurityShow, SecurityEdit} from './security'
import {  SecurityResultsList, SecurityResultsShow } from './securityResults';


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
        <Resource name="extractor" list={ExtractorList} edit={ExtractorEdit} create={ExtractorCreate} show={ExtractorShow}/>
        <Resource name="lighthouse" title="Lighthouse" options={{ title: 'lighthouse', label: 'Lighthouse' }} list={LighthouseList} show={LighthouseShow}  edit={LighthouseEdit} create={LighthouseCreate}/>
        <Resource name="lighthouse_details" title="Lighthouse" options={{ title: 'lighthouse', label: 'Lighthouse Results' }} list={LighthouseResultsList} show={LighthouseResultsShow} />
        <Resource name="keywords/yake" options={{ label: 'Yake' }}  list={YakeList} show={YakeShow} create={YakeCreate} edit={yakeEdit}/>
        <Resource name="sitemap" options={{ label: 'Sitemap' }}  list={SitemapList} show={SitemapShow}  create={SitemapCreate} edit={SitemapEdit}/>
        <Resource name="summarize" options={{ label: 'Sitemap' }}  list={BertList} show={BertShow} create={BertCreate} edit={BertEdit} />
        <Resource name="security" title="Security" options={{ title: 'security', label: 'Security' }} list={SecurityList} show={SecurityShow}  edit={SecurityEdit} create={SecurityCreate}/>
        <Resource name="security_details" title="Security" options={{ title: 'security', label: 'Security Results' }} list={SecurityResultsList} show={SecurityResultsShow} />
    </Admin>
);

export default App;