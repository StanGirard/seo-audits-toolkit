import * as React from "react";
import { AutocompleteInput, Create, SimpleForm, TextInput } from 'react-admin';

export const ExtractorCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="url" />
            <AutocompleteInput source="type_audit" choices={[
                { id: 'HEADERS', name: 'Headers' },
                { id: 'IMAGES', name: 'Images' },
                { id: 'LINKS', name: 'Links' },
            ]} />
        </SimpleForm>
    </Create>
)