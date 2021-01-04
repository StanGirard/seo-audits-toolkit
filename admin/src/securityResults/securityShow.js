import * as React from "react";
import { DeleteButton,ArrayField,Datagrid,UrlField,BooleanField, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
import { green } from '@material-ui/core/colors';



export const SecurityResultsShow = (props) => {

    return (
        <Show {...props}>
            <SimpleShowLayout>
                <MyUrlField source="url" />
                <TextField source="score" />
                <ArrayField source="result.tests" fieldKey="name" >
                    <Datagrid>
                        <TextField source="name" />
                        <BooleanField source="pass"  />
                        <TextField source="score_description"/>
                    </Datagrid>
                </ArrayField>
                <ArrayField source="result.response_headers" fieldKey="name" >
                    <Datagrid>
                        <TextField source="name" />
                        <TextField source="value"/>
                    </Datagrid>
                </ArrayField>
                
                <EditButton />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};
