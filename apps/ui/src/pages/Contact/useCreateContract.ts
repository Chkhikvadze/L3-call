import { useContext, useEffect, useState } from 'react'

import { useContactsService } from 'services/contact/useContactsService'

import { ToastContext } from 'contexts'
import { useModal } from 'hooks'

import { useFormik } from 'formik'
import { useNavigate } from 'react-router-dom'
import { useCreateContactService } from 'services/contact/useCreateContactService'

export const useCreateContact = () => {
  const navigate = useNavigate()

  const { setToast } = useContext(ToastContext)
  const { openModal, closeModal } = useModal()

  const [isLoading, setIsLoading] = useState(false)

  const [createContactService] = useCreateContactService()

  const { data: contacts, refetch: refetchContacts } = useContactsService()

  const initialValues = {
    contact_name: '',
    contact_description: '',
    contact_group_id: '132306b9-e428-4534-b744-aa8cdf86d1e6',
    contact_email: '',
    contact_phone: '',
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

      await createContactService(contactInput)

      await refetchContacts()
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
    initialValues: initialValues,

    onSubmit: async values => handleSubmit(values),
  })

  return {
    contacts,
    formik,
    isLoading,
  }
}
