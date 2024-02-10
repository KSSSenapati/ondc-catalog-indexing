import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import Image from "react-bootstrap/Image";

export const ImageUpload = ({setImageFile}) => {
    const [selectedFile, setSelectedFile] = useState()
    const [preview, setPreview] = useState()

    useEffect(() => {
        if (!selectedFile) {
            setPreview(undefined)
            return
        }

        const objectUrl = URL.createObjectURL(selectedFile)
        setPreview(objectUrl)

        return () => URL.revokeObjectURL(objectUrl)
    }, [selectedFile])

    const onSelectFile = e => {
        if (!e.target.files || e.target.files.length === 0) {
            setSelectedFile(undefined)
            return
        }

        setSelectedFile(e.target.files[0])
        setImageFile(e.target.files);
    }

    return (
        <>
        <Form.Group controlId="formFile" className="mb-3">
            {selectedFile &&  <Image src={preview}  style={{width: "100%", padding:"10%", alignSelf:"center"}} rounded/> }
            <Form.Label>Upload Image</Form.Label>
            <Form.Control type="file" onChange={onSelectFile} accept=".png, .jpg, .jpeg"/>
        </Form.Group>
        </>
    )
}