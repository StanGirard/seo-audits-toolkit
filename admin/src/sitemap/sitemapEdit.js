import * as React from "react";
import { Edit, SimpleForm, TextInput, ArrayInput, SimpleFormIterator, NumberInput, DateInput } from 'react-admin';



export const SitemapEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="website" />
            <TextInput source="url" />
            <ArrayInput source="result">
                <SimpleFormIterator>
                    <TextInput source="id" />
                    <NumberInput source="org" />
                    <TextInput source="url" />
                    <DateInput source="last_modified" />
                </SimpleFormIterator>
            </ArrayInput>
            <TextInput source="status_job" />
            <DateInput source="begin_date" />
        </SimpleForm>
    </Edit>
);