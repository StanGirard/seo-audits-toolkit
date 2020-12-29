import * as React from "react";
import { AutocompleteInput,NumberInput, Create, SimpleForm, TextInput, useNotify, useRefresh } from 'react-admin';

export const YakeCreate = props => {

    const notify = useNotify();
    const refresh = useRefresh();

    const onFailure = (error) => {
        notify(`Could not edit post: ${error.message}`)
        refresh();
    };
    return (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="name" />
            <TextInput source="text" />
            <NumberInput source="ngram" step={1}/>
            <AutocompleteInput source="language" choices={[
                { id: 'en', name: 'English' },
            ]} />
            <NumberInput source="number_keywords" step={1} />
        </SimpleForm>
    </Create>
    )
}