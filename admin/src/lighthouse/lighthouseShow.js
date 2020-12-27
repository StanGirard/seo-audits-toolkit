import * as React from "react";
import { BooleanField, DeleteButton, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';

export const LighthouseShow = (props) => {
    
    return (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="url" />
            <BooleanField source="scheduled" />
            <EditButton/>
            <DeleteButton />
        </SimpleShowLayout>
    </Show>
)};
