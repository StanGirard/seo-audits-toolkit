import React from 'react';
import { connect } from 'react-redux';
import Loader from "../../components/Loader"
import Table from 'react-bootstrap/Table'
import "../../css/keywords.css"

export class Keywords extends React.Component {



    componentDidMount() {
        console.log("HAHIHI")
        const { keywords, dispatch } = this.props;
        if (keywords.status !== "SUCCESS" && keywords.status !== "PENDING") {
            console.log("HAHAHAHAHAHAHAHAHAHAHA")
            dispatch({ type: "KEYWORDS_GET" });
        }

    }

    componentDidUpdate() {
        const { dispatch, keywords } = this.props;
    }
    render() {
        console.log("HEHEHEHELOLOLO")

        const { keywords } = this.props;
        console.log(keywords)
        if (keywords.status === "SUCCESS") {
            return (

                <div className="keywords">
                    <Table striped bordered hover >
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Query</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {keywords.data.results.map((value) => (
                                <tr>
                                    <td>{value.id}</td>
                                    <td>{value.query}</td>
                                    <td>{value.status_job}</td>
                                </tr>
                            ))}

                        </tbody>
                    </Table>
                </div>




            )
        }
        if (keywords.status === "PENDING") {
            return (
                <Loader />
            )
        }

        else {
            return (
                <div>
                    {keywords.status}
                </div>)

        }


    }

};
function mapStateToProps(state) {
    return { keywords: state.keywords };
}

export default connect(mapStateToProps)(Keywords);