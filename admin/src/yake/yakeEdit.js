import * as React from "react";
import { Edit, SimpleForm, TextInput, ArrayInput, SimpleFormIterator, NumberInput, DateInput } from 'react-admin';


export const yakeEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="text" />
            <TextInput source="website" />
            <TextInput source="name" />
            <ArrayInput source="result">
                <SimpleFormIterator>
                    <TextInput source="id" />
                    <TextInput source="ngram" />
                    <NumberInput source="score" />
                </SimpleFormIterator>
            </ArrayInput>
            <NumberInput source="ngram" />
            <TextInput source="language" />
            <NumberInput source="number_keywords" />
            <TextInput source="status_job" />
            <DateInput source="last_updated" />
        </SimpleForm>
    </Edit>
);