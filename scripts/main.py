from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from customtkinter import filedialog
from PIL import Image

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PostScheduler")
        self.geometry("500x400")
        self.resizable(False, False)


        self.iconbitmap("assets/iconphoto.ico")
        

        self.label_header = ctk.CTkLabel(self, text="PostScheduler", font=("Raleway", 24))
        self.label_subheader = ctk.CTkLabel(self, text="Escolha a rede social:", font=("Raleway", 14))

        self.button_instagram = ctk.CTkButton(self, text="Instagram", font=("Raleway", 14), command=self.instagram,fg_color="#000000",hover_color="#0F1419")
        self.button_linkedln = ctk.CTkButton(self, text="X", font=("Raleway", 14), command=self.x,fg_color="#000000",hover_color="#0F1419")
        self.button_x = ctk.CTkButton(self, text="Linkedln", font=("Raleway", 14), command=self.linkedin,fg_color="#000000",hover_color="#0F1419")

        self.button_addcredencials = ctk.CTkButton(self, text="Adicionar Credenciais", font=("Raleway", 14), command=self.add_credencials,fg_color="#000000",hover_color="#0F1419")
        self.label_credencials = ctk.CTkLabel(self, text="Credenciais não identificadas", font=("Raleway", 14))


        self.label_header.pack(pady=5)
        self.label_subheader.pack(pady=5)
        self.button_instagram.pack(pady=10)
        self.button_linkedln.pack(pady=10)
        self.button_x.pack(pady=10)
        self.label_credencials.pack(pady=5,side=BOTTOM)
        self.button_addcredencials.pack(pady=5,side=BOTTOM)


    def add_credencials(self):
        def save_credentials():
            username = credencial_window.entry_username.get()
            password = credencial_window.entry_password.get()
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("USE PostManager;")
                cursor.execute("SELECT COUNT(*) FROM credencials")
                row_count = cursor.fetchone()[0]
                if row_count < 6:
                    cursor.execute("INSERT INTO credencials (username, password) VALUES (?,?)",(username, password))
                    cursor.close()
                    credencial_window.entry_username.delete(0, END)
                    credencial_window.entry_password.delete(0, END)
                    messagebox.showinfo("Info", "Credenciais adicionadas com sucesso",parent=credencial_window)
                else:
                    messagebox.showinfo("Info", "Limite de credenciais atingido",parent=credencial_window)

        def close_window():
            self.deiconify()
            credencial_window.destroy()
            

        def manage_credentials():
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM credencials")
                row_count = cursor.fetchone()[0]
                if row_count == 0:
                    messagebox.showinfo("Info", "Nenhuma credencial encontrada",parent=credencial_window)
                    return
                credencial_window.withdraw()
                manage_window = ctk.CTkToplevel(credencial_window)
                manage_window.title("Manage Credencials")
                manage_window.geometry("540x460")
                manage_window.iconbitmap("assets/iconphoto.ico")
                connection = connect_db()
                row_grid = 0
                column_grid = 0
                buttons = []

                cursor.execute("SELECT * FROM credencials")
                result = cursor.fetchall()

                def select_as_principal(index):
                    try:
                        self.username = result[index][1]
                        self.password = result[index][2]
                        self.label_credencials.configure(text=f"Username: {self.username} | Password: {self.password}",text_color="#66FF00")
                        messagebox.showinfo("Info", f"Selected {self.username} as principal",parent=manage_window)
                    except Exception as e:
                        messagebox.showerror("Info", f"Erro: {e}",parent=manage_window)


                def delete(index):
                    try:
                        cursor.execute("SELECT COUNT(*) FROM credencials")
                        if cursor.fetchone()[0] == 1:
                            messagebox.showinfo("Info", "Não é possível deletar a única credencial",parent=manage_window)
                            return
                        userid = result[index][0]
                        cursor.execute("DELETE FROM credencials WHERE UserID = ?",(userid,))
                        manage_window.destroy()
                        manage_credentials()
                    except Exception as e:
                        messagebox.showerror("Info", f"Erro: {e}",parent=manage_window)

                def update(index):
                    try:
                        userid = result[index][0]

                        def save():
                            new_username = entryusername.get()
                            new_password = entrypassword.get()
                            cursor.execute("UPDATE credencials SET username = ?, password = ? WHERE UserID = ?",(new_username,new_password,userid))
                            manage_window.destroy()
                            manage_credentials()

                        def cancel():
                            update_window.destroy()
                            manage_window.deiconify()

                        manage_window.withdraw()
                        update_window = ctk.CTkToplevel(manage_window)
                        update_window.title("Update Credencial")
                        update_window.geometry("337x192")
                        update_window.iconbitmap("assets/iconphoto.ico")
                        labelusername = ctk.CTkLabel(update_window, text="Usuário:", font=("Raleway", 12))
                        labelusername.grid(pady=10,padx=10,row=0,column=0)
                        labelpassword = ctk.CTkLabel(update_window, text="Senha:", font=("Raleway", 12))
                        labelpassword.grid(pady=10,padx=10,row=1,column=0)
                        entryusername = ctk.CTkEntry(update_window, font=("Raleway", 12))
                        entryusername.grid(pady=10,padx=10,row=0,column=1)
                        entrypassword = ctk.CTkEntry(update_window, font=("Raleway", 12))
                        entrypassword.grid(pady=10,padx=10,row=1,column=1)
                        save_button = ctk.CTkButton(update_window, text="Save", font=("Raleway", 12),command=save,fg_color="#000000",hover_color="#0F1419")
                        cancel_button = ctk.CTkButton(update_window, text="Cancel", font=("Raleway", 12),command=cancel,fg_color="#000000",hover_color="#0F1419")
                        save_button.grid(pady=10,padx=10,row=2,column=0)
                        cancel_button.grid(pady=10,padx=10,row=2,column=1)
                    except Exception as e:
                        messagebox.showerror("Info", f"Erro: {e}",parent=manage_window)

                def close_manage_window():
                    manage_window.destroy()
                    credencial_window.deiconify()
                    

                for idx,row in enumerate(result):
                    username, password = row[1], row[2]

                    def delete_mode(button):
                        for i,button in enumerate(buttons):
                            button.configure(fg_color="#e02a1d",command=lambda i=i: delete(i), text="Delete",hover_color="#4d0000")

                    def update_mode(button):
                        for i,button in enumerate(buttons):
                            button.configure(fg_color="#b58a07",command=lambda i=i: update(i), text="Update",hover_color="#4d3b00")

                    def select(button):
                        for i,button in enumerate(buttons):
                            button.configure(fg_color="#134510",command=lambda i=i: select_as_principal(i), text="Select as Principal",hover_color="#0d240b")

                    frame = ctk.CTkFrame(manage_window,width=30,height=10)
                    labelusername = ctk.CTkLabel(frame, text=username, font=("Raleway", 12))
                    labelpassword = ctk.CTkLabel(frame, text=password, font=("Raleway", 12))
                    button = ctk.CTkButton(frame, text="Select as Principal", font=("Raleway", 12),fg_color="#134510", command=lambda idx=idx: select_as_principal(idx),hover_color="#0d240b")
                    buttons.append(button)
                    frame.grid(row=row_grid,column=column_grid,padx=10,pady=10)
                    labelusername.grid(row=0,column=0,pady=10,padx=10)
                    labelpassword.grid(row=1,column=0,pady=10,padx=10)
                    button.grid(rowspan=2,row=2,pady=10,padx=10)
                    
                    if column_grid == 2:
                        column_grid = 0
                        row_grid += 1
                    else:
                        column_grid += 1

                button_delete = ctk.CTkButton(manage_window, text="Delete mode", font=("Raleway", 12), command=lambda: delete_mode(button),fg_color="#000000",hover_color="#0F1419")
                button_update = ctk.CTkButton(manage_window, text="Update mode", font=("Raleway", 12), command=lambda: update_mode(button),fg_color="#000000",hover_color="#0F1419")
                button_select = ctk.CTkButton(manage_window, text="Select mode", font=("Raleway", 12), command=lambda: select(button),fg_color="#000000",hover_color="#0F1419")
                button_delete.grid(pady=10, padx=10, row=3, column=0)
                button_update.grid(pady=10, padx=10, row=3, column=1)
                button_select.grid(pady=10, padx=10, row=3, column=2)

                button_close = ctk.CTkButton(manage_window, text="Close", font=("Raleway", 12), command=close_manage_window,fg_color="#e02a1d",hover_color="#4d0000")
                button_close.grid(pady=10, padx=10, row=4, column=1)
            connection.close()

        self.withdraw()
        credencial_window = ctk.CTkToplevel(self)
        credencial_window.title("Adicionar Credenciais")
        credencial_window.geometry("230x250")
        credencial_window.resizable(False, False)
        credencial_window.iconbitmap("assets/iconphoto.ico")

        credencial_window.label_username = ctk.CTkLabel(credencial_window, text="Usuário:", font=("Raleway", 12))
        credencial_window.label_username.grid(pady=10,padx=10,row=0,column=0)
        credencial_window.label_password = ctk.CTkLabel(credencial_window, text="Senha:", font=("Raleway", 12))
        credencial_window.label_password.grid(pady=10,padx=10,row=1,column=0)
        credencial_window.entry_username = ctk.CTkEntry(credencial_window, font=("Raleway", 12))
        credencial_window.entry_username.grid(pady=10,padx=10,row=0,column=1)
        credencial_window.entry_password = ctk.CTkEntry(credencial_window, font=("Raleway", 12))
        credencial_window.entry_password.grid(pady=10,padx=10,row=1,column=1)

        credencial_window.button_save = ctk.CTkButton(credencial_window, text="Add", font=("Raleway", 12),command=save_credentials,fg_color="#000000",hover_color="#0F1419")
        credencial_window.button_save.grid(pady=10,padx=10,columnspan=2,row=2,column=0)

        credencial_window.manage_credentials = ctk.CTkButton(credencial_window, text="Manage", font=("Raleway", 12),command=manage_credentials,fg_color="#000000",hover_color="#0F1419")
        credencial_window.manage_credentials.grid(padx=10,pady=10,columnspan=2,row=3,column=0)

        credencial_window.close_window = ctk.CTkButton(credencial_window, text="Close", font=("Raleway", 12),command=close_window,fg_color="#000000",hover_color="#0F1419")
        credencial_window.close_window.grid(padx=10,pady=10,columnspan=2,row=4,column=0)


    def instagram(self):
        try:
            def destroy_window():
                Instagram_window.destroy()
                self.deiconify()

            def post_instagram():
                def instagram_get_image():
                    file_path = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.png *.jpg *.jpeg")],
                    )
                    if file_path:
                        image = Image.open(file_path)
                        image = image.resize((100, 100))
                        ctk_image = ctk.CTkImage(light_image=image)
                        label_image.configure(image=ctk_image)
                        label_image.image = ctk_image
                        messagebox.showinfo("Info", "Imagem adicionada com sucesso",parent=post_instagram_window)

                post_instagram_window = ctk.CTkToplevel(Instagram_window)
                post_instagram_window.title("Instagram Post")
                post_instagram_window.geometry("400x300")
                post_instagram_window.iconbitmap("assets/iconphoto.ico")
                post_instagram_window.resizable(False, False)

                label_header = ctk.CTkLabel(post_instagram_window, text="Instagram Post", font=("Raleway", 24))
                label_subheader = ctk.CTkLabel(post_instagram_window, text="Escreva a legenda:", font=("Raleway", 14))
                entry_caption = ctk.CTkEntry(post_instagram_window, font=("Raleway", 12))
                button_filedialog = ctk.CTkButton(post_instagram_window, text="Adicionar foto", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=instagram_get_image)
                label_image= ctk.CTkLabel(post_instagram_window,text="", height=100, width=100)
                button_post = ctk.CTkButton(post_instagram_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")

                label_header.pack(pady=5)
                label_subheader.pack(pady=5)
                entry_caption.pack(pady=5)
                button_filedialog.pack(pady=5)
                label_image.pack(pady=5)
                button_post.pack(pady=5,side=BOTTOM)



            if self.label_credencials.cget("text") == "Credenciais não identificadas":
                messagebox.showinfo("Info", "Por favor adicione credenciais",parent=self)
                return
            print(self.username,self.password) 
            self.withdraw()
            Instagram_window = ctk.CTkToplevel(self)
            Instagram_window.title("Instagram configuration")
            Instagram_window.geometry("400x300")
            Instagram_window.iconbitmap("assets/iconphoto.ico")
            Instagram_window.resizable(False, False)


            Instagram_window.label_header = ctk.CTkLabel(Instagram_window, text="Instagram", font=("Raleway", 24))
            Instagram_window.label_subheader = ctk.CTkLabel(Instagram_window, text="Escolha a ação:", font=("Raleway", 14))
            Instagram_window.button_post = ctk.CTkButton(Instagram_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=post_instagram)
            Instagram_window.button_schedule = ctk.CTkButton(Instagram_window, text="Agendar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")
            Instagram_window.button_close = ctk.CTkButton(Instagram_window, text="Close", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=destroy_window)
            Instagram_window.label_header.pack(pady=5)
            Instagram_window.label_subheader.pack(pady=5)
            Instagram_window.button_post.pack(pady=10)
            Instagram_window.button_schedule.pack(pady=10)
            Instagram_window.button_close.pack(pady=10,side=BOTTOM)
        except Exception as e:
            messagebox.showerror("Info", f"Erro: {e}",parent=self)


    def x(self):
        try:
            def destroy_window():
                X_window.destroy()
                self.deiconify()

            def post_x():
                def x_get_image():
                    file_path = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.png *.jpg *.jpeg")],
                    )
                    if file_path:
                        image = Image.open(file_path)
                        image = image.resize((100, 100))
                        ctk_image = ctk.CTkImage(light_image=image)
                        label_image.configure(image=ctk_image)
                        label_image.image = ctk_image
                        messagebox.showinfo("Info", "Imagem adicionada com sucesso",parent=post_x_window)


                post_x_window = ctk.CTkToplevel(X_window)
                post_x_window.title("Instagram Post")
                post_x_window.geometry("400x300")
                post_x_window.iconbitmap("assets/iconphoto.ico")
                post_x_window.resizable(False, False)

                label_header = ctk.CTkLabel(post_x_window, text="Instagram Post", font=("Raleway", 24))
                label_subheader = ctk.CTkLabel(post_x_window, text="Escreva a legenda:", font=("Raleway", 14))
                entry_caption = ctk.CTkEntry(post_x_window, font=("Raleway", 12))
                button_filedialog = ctk.CTkButton(post_x_window, text="Adicionar foto", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=x_get_image)
                label_image = ctk.CTkLabel(post_x_window,text="", height=100, width=100)
                button_post = ctk.CTkButton(post_x_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")

                label_header.pack(pady=5)
                label_subheader.pack(pady=5)
                entry_caption.pack(pady=5)
                button_filedialog.pack(pady=5)
                label_image.pack(pady=5)
                button_post.pack(pady=5,side=BOTTOM)

            if self.label_credencials.cget("text") == "Credenciais não identificadas":
                messagebox.showinfo("Info", "Por favor adicione credenciais",parent=self)
                return
            self.withdraw()

            X_window = ctk.CTkToplevel(self)
            X_window.title("X configuration")
            X_window.geometry("400x300")
            X_window.iconbitmap("assets/iconphoto.ico")
            X_window.resizable(False, False)
            X_window.label_header = ctk.CTkLabel(X_window, text="X", font=("Raleway", 24))
            X_window.label_subheader = ctk.CTkLabel(X_window, text="Escolha a ação:", font=("Raleway", 14))
            X_window.button_post = ctk.CTkButton(X_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=post_x)
            X_window.button_schedule = ctk.CTkButton(X_window, text="Agendar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")
            X_window.button_close = ctk.CTkButton(X_window, text="Close", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=destroy_window)
            X_window.label_header.pack(pady=5)
            X_window.label_subheader.pack(pady=5)
            X_window.button_post.pack(pady=10)
            X_window.button_schedule.pack(pady=10)
            X_window.button_close.pack(pady=10,side=BOTTOM)
        except Exception as e:
            messagebox.showerror("Info", f"Erro: {e}",parent=self)


    def linkedin(self):
        try:
            def destroy_window():
                Likendin_window.destroy()
                self.deiconify()

            def post_linkedin():
                def linkedin_get_image():
                    file_path = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.png *.jpg *.jpeg")],
                    )
                    if file_path:
                        image = Image.open(file_path)
                        image = image.resize((100, 100))
                        ctk_image = ctk.CTkImage(light_image=image)
                        label_image.configure(image=ctk_image)
                        label_image.image = ctk_image
                        messagebox.showinfo("Info", "Imagem adicionada com sucesso",parent=post_likendin_window)


                post_likendin_window = ctk.CTkToplevel(Likendin_window)
                post_likendin_window.title("Instagram Post")
                post_likendin_window.geometry("400x300")
                post_likendin_window.iconbitmap("assets/iconphoto.ico")
                post_likendin_window.resizable(False, False)

                label_header = ctk.CTkLabel(post_likendin_window, text="LinkedIn Post", font=("Raleway", 24))
                label_subheader = ctk.CTkLabel(post_likendin_window, text="Escreva a legenda:", font=("Raleway", 14))
                entry_caption = ctk.CTkEntry(post_likendin_window, font=("Raleway", 12))
                button_get_image = ctk.CTkButton(post_likendin_window, text="Adicionar foto", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=linkedin_get_image)
                label_image = ctk.CTkLabel(post_likendin_window,text="", height=100, width=100)
                button_post = ctk.CTkButton(post_likendin_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")

                label_header.pack(pady=5)
                label_subheader.pack(pady=5)
                entry_caption.pack(pady=5)
                button_get_image.pack(pady=5)
                label_image.pack(pady=5)
                button_post.pack(pady=5,side=BOTTOM)


                
            if self.label_credencials.cget("text") == "Credenciais não identificadas":
                messagebox.showinfo("Info", "Por favor adicione credenciais",parent=self)
                return
            self.withdraw()

            Likendin_window = ctk.CTkToplevel(self)
            Likendin_window.title("LinkedIn configuration")
            Likendin_window.geometry("400x300")
            Likendin_window.iconbitmap("assets/iconphoto.ico")
            Likendin_window.resizable(False, False)
            Likendin_window.label_header = ctk.CTkLabel(Likendin_window, text="LinkedIn", font=("Raleway", 24))
            Likendin_window.label_subheader = ctk.CTkLabel(Likendin_window, text="Escolha a ação:", font=("Raleway", 14))
            Likendin_window.button_post = ctk.CTkButton(Likendin_window, text="Postar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=post_linkedin)
            Likendin_window.button_schedule = ctk.CTkButton(Likendin_window, text="Agendar", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419")
            Likendin_window.button_close = ctk.CTkButton(Likendin_window, text="Close", font=("Raleway", 14),fg_color="#000000",hover_color="#0F1419",command=destroy_window)
            Likendin_window.label_header.pack(pady=5)
            Likendin_window.label_subheader.pack(pady=5)
            Likendin_window.button_post.pack(pady=10)
            Likendin_window.button_schedule.pack(pady=10)
            Likendin_window.button_close.pack(pady=10,side=BOTTOM)
        except Exception as e:
            messagebox.showerror("Info", f"Erro: {e}",parent=self)

if __name__ == "__main__":
    app = Main()
    app.mainloop()