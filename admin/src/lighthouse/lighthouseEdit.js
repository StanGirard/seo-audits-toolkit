import * as React from "react";
import { BooleanInput, TextInput, Edit, SimpleForm, DateInput } from 'react-admin';



export const LighthouseEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="url" />
            <TextInput source="website" />
            <BooleanInput source="scheduled" />
            <DateInput source="last_updated" />
        </SimpleForm>
    </Edit>
);