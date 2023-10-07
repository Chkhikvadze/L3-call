import { ToastContext } from 'contexts'
import { useFormik } from 'formik'

import { useContext, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { useContactByIdService } from 'services/contact/useContactByIdService'

export const useEditContact = () => {
  const { setToast } = useContext(ToastContext)

  const navigate = useNavigate()
  const params = useParams()

  const { contactId } = params

  const [isLoading, setIsLoading] = useState(false)

  const { data: contactById } = useContactByIdService({ id: contactId || '' })

  const defaultValues = {
    contact_name: contactById?.name,
    contact_description: contactById?.description,
    contact_group_id: contactById?.group_id,
    contact_email: contactById?.email,
    contact_phone: contactById?.phone,
  }

  const handleSubmit = async (values: any) => {
    setIsLoading(true)
    try {
      const contactInput = {
        name: values.contact_name,
        description: values.contact_description,
        group_id: values.contact_group_id,
        email: values.contact_email,
        phone: values.contact_phone,
      }

      // await createContactService(contactInput)

      // await refetchContacts()
      setToast({
        message: 'New Contact was Created!',
        type: 'positive',
        open: true,
      })
      navigate('/contacts')
    } catch (e) {
      setToast({
        message: 'Failed To Add Contact!',
        type: 'negative',
        open: true,
      })
    }
    setIsLoading(false)
  }
  const formik = useFormik({
    initialValues: defaultValues,
    enableReinitialize: true,

    onSubmit: async values => handleSubmit(values),
  })

  return {
    formik,
    isLoading,
  }
}
