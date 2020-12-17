import * as React from 'react';
import {
    Filter,
    AutocompleteInput
} from 'react-admin';


export const ExtractorFilter = props => (
    <Filter {...props}>
        <AutocompleteInput source="type_audit" choices={[
            { id: 'HEADERS', name: 'Headers' },
            { id: 'IMAGES', name: 'Images' },
            { id: 'LINKS', name: 'Links' },
]} />
        
    </Filter>
);