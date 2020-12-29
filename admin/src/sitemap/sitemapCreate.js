import * as React from "react";
import { Create, ReferenceInput, SelectInput, SimpleForm, TextInput, useNotify, useRefresh } from 'react-admin';

export const SitemapCreate = props => {

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
            </SimpleForm>
        </Create>
    )
}