import * as React from "react";
import { BooleanInput, Create, SimpleForm, TextInput, useNotify, useRefresh } from 'react-admin';

export const LighthouseCreate = props => {

    const notify = useNotify();
    const refresh = useRefresh();

    const onFailure = (error) => {
        notify(`Could not edit post: ${error.message}`)
        refresh();
    };
    return (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="url" />
            <BooleanInput source="scheduled"/>
        </SimpleForm>
    </Create>
    )
}