import * as React from "react";
import { BooleanField, DeleteButton, EditButton, Show, SimpleShowLayout, TextField, IntegerField } from 'react-admin';
import { DataGrid } from '@material-ui/data-grid';




const MyUrlField = ({ record = {}, source }) => {


    return (
        <div style={{ display: 'flex', height: '500px' }}>
            <div style={{ flexGrow: 1 }}>
                {(JSON.parse(record[source].length > 0)) ?
                    <DataGrid
                    columns={[{ field: 'id' }, { field: "ngram" ,width: 300}, { field: 'score',width: 150 }]}
                    rows={JSON.parse(record[source])}
                     density="compact"/>
                : <div> Still calculating - Please refresh in a couple of seconds </div>
            }
                
            </div>
        </div>
    );
}
export const YakeShow = (props) => {

    return (
        <Show {...props}>
            <SimpleShowLayout>
                <TextField source="id" />
                <TextField source="name" />
                <MyUrlField source="result" />
                <EditButton />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};