import * as React from "react";
import { DeleteButton, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
export const LighthouseResultsShow = (props) => {

    return (
        <Show {...props}>
            <SimpleShowLayout>
                <MyUrlField source="url" />
                <TextField source="accessibility_score" />
                <TextField source="best_practices_score" />
                <TextField source="performance_score" />
                <TextField source="pwa_score" />
                <TextField source="seo_score" />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};
