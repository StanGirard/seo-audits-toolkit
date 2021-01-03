import * as React from "react";
import { BooleanInput, Create, SimpleForm, TextInput, useNotify, useRefresh, ReferenceInput, SelectInput } from 'react-admin';

export const SecurityCreate = props => {

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
            <BooleanInput source="scheduled"/>
        </SimpleForm>
    </Create>
    )
}