import * as React from "react";
import { AutocompleteInput, Create, SimpleForm, TextInput, ReferenceInput, SelectInput, useNotify, useRefresh } from 'react-admin';

export const ExtractorCreate = props => {

    const notify = useNotify();
    const refresh = useRefresh();

    const onFailure = (error) => {
        notify(`Could not edit post: ${error.message}`)
        refresh();
    };
    return (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="website_name" reference="website_user">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="url" />
            <AutocompleteInput source="type_audit" choices={[
                { id: 'HEADERS', name: 'Headers' },
                { id: 'IMAGES', name: 'Images' },
                { id: 'LINKS', name: 'Links' },
            ]} />
        </SimpleForm>
    </Create>
    )
}