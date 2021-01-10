import * as React from "react";
import { Edit, SimpleForm, TextInput, DateInput } from 'react-admin';


export const ExtractorEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="website" />
            <TextInput source="url" />
            <TextInput source="result" />
            <TextInput source="type_audit" />
            <TextInput source="status_job" />
            <DateInput source="begin_date" />
        </SimpleForm>
    </Edit>
);